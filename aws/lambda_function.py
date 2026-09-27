import csv
import io
import re
from datetime import datetime

REQUIRED_COLUMNS = [
    'order_number', 'customer_id', 'order_date', 
    'status', 'product_sku', 'quantity', 'unit_price', 'payment_method'
]

VALID_STATUSES = {'PENDING', 'CONFIRMED', 'SHIPPED', 'DELIVERED', 'CANCELLED'}


def validate_and_transform_records(csv_content):
    """
    Validates CSV records line-by-line against business rules and data quality constraints.
    Returns:
        valid_records (list): Enriched valid records
        rejected_records (list): Records with error details
        summary (dict): Execution metrics
    """
    reader = csv.DictReader(io.StringIO(csv_content))
    
    # 1. Header Validation
    if not reader.fieldnames:
        return [], [{'error': 'EMPTY_FILE', 'reason': 'CSV file is empty or missing header.'}], {
            'total_rows': 0, 'valid_rows': 0, 'rejected_rows': 1
        }

    missing_cols = [col for col in REQUIRED_COLUMNS if col not in reader.fieldnames]
    if missing_cols:
        return [], [{'error': 'SCHEMA_MISMATCH', 'reason': f'Missing required columns: {missing_cols}'}], {
            'total_rows': 0, 'valid_rows': 0, 'rejected_rows': 1
        }

    valid_records = []
    rejected_records = []
    seen_order_numbers = set()
    row_index = 1

    for row in reader:
        row_index += 1
        errors = []

        # Check required fields
        for col in REQUIRED_COLUMNS:
            val = row.get(col)
            if val is None or str(val).strip() == '':
                errors.append(f"Missing mandatory field '{col}'")

        if errors:
            rejected_records.append({
                'row_number': row_index,
                'data': row,
                'reasons': errors
            })
            continue

        order_num = row['order_number'].strip()
        cust_id_str = row['customer_id'].strip()
        date_str = row['order_date'].strip()
        status = row['status'].strip().upper()
        sku = row['product_sku'].strip()
        qty_str = row['quantity'].strip()
        price_str = row['unit_price'].strip()
        payment = row['payment_method'].strip()

        # Uniqueness check within batch
        if order_num in seen_order_numbers:
            errors.append(f"Duplicate order_number '{order_num}' detected in batch.")
        else:
            seen_order_numbers.add(order_num)

        # Customer ID check
        try:
            cust_id = int(cust_id_str)
            if cust_id <= 0:
                errors.append("customer_id must be a positive integer.")
        except ValueError:
            errors.append(f"Invalid customer_id format '{cust_id_str}'.")

        # Date format check
        valid_date = False
        parsed_date = None
        for fmt in ('%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S'):
            try:
                parsed_date = datetime.strptime(date_str, fmt)
                valid_date = True
                break
            except ValueError:
                continue
        if not valid_date:
            errors.append(f"Invalid order_date format '{date_str}'. Expected YYYY-MM-DD.")

        # Status check
        if status not in VALID_STATUSES:
            errors.append(f"Invalid status '{status}'. Must be one of {sorted(list(VALID_STATUSES))}.")

        # Quantity check
        qty = 0
        try:
            qty = int(qty_str)
            if qty <= 0:
                errors.append("quantity must be greater than 0.")
        except ValueError:
            errors.append(f"Invalid quantity value '{qty_str}'.")

        # Unit Price check
        unit_price = 0.0
        try:
            unit_price = float(price_str)
            if unit_price < 0:
                errors.append("unit_price cannot be negative.")
        except ValueError:
            errors.append(f"Invalid unit_price value '{price_str}'.")

        if errors:
            rejected_records.append({
                'row_number': row_index,
                'order_number': order_num,
                'data': row,
                'reasons': errors
            })
        else:
            # Transformation & Financial Enrichment
            subtotal = round(qty * unit_price, 2)
            tax = round(subtotal * 0.08, 2)
            shipping = 10.00 if subtotal < 100.00 else 0.00
            total = round(subtotal + tax + shipping, 2)

            valid_records.append({
                'order_number': order_num,
                'customer_id': cust_id,
                'order_date': parsed_date.strftime('%Y-%m-%d %H:%M:%S'),
                'status': status,
                'product_sku': sku,
                'quantity': qty,
                'unit_price': unit_price,
                'subtotal': subtotal,
                'tax_amount': tax,
                'shipping_fee': shipping,
                'total_amount': total,
                'payment_method': payment
            })

    total_rows = len(valid_records) + len(rejected_records)
    summary = {
        'total_rows_processed': total_rows,
        'valid_records_count': len(valid_records),
        'rejected_records_count': len(rejected_records),
        'pass_rate_percentage': round((len(valid_records) / total_rows * 100), 2) if total_rows > 0 else 0.0
    }

    return valid_records, rejected_records, summary


def lambda_handler(event, context=None):
    """
    AWS Lambda Handler entry point for S3 ObjectCreated events or direct invocation.
    """
    print("Received event:", event)

    # In production AWS, event contains Records with s3 bucket and key.
    # In simulation or test payload, csv_content or records may be passed directly.
    csv_content = ""

    if 'Records' in event and len(event['Records']) > 0:
        # Simulated S3 Event
        s3_record = event['Records'][0].get('s3', {})
        bucket_name = s3_record.get('bucket', {}).get('name', 'retail-orders-raw-bucket')
        object_key = s3_record.get('object', {}).get('key', 'batch_orders.csv')
        print(f"Processing object s3://{bucket_name}/{object_key}")
        
        # If payload provides simulated content
        csv_content = event.get('mock_s3_file_content', '')
    elif 'csv_content' in event:
        csv_content = event['csv_content']
    else:
        return {
            'statusCode': 400,
            'body': {'error': 'No CSV content or S3 record provided.'}
        }

    valid_records, rejected_records, summary = validate_and_transform_records(csv_content)

    return {
        'statusCode': 200,
        'summary': summary,
        'valid_records': valid_records,
        'rejected_records': rejected_records
    }
