import pytest
from aws.lambda_function import validate_and_transform_records, lambda_handler

def test_lambda_validation_valid_csv():
    valid_csv = """order_number,customer_id,order_date,status,product_sku,quantity,unit_price,payment_method
ORD-2026-9001,1,2026-03-25 10:00:00,PENDING,SKU-ELEC-1001,2,149.99,Credit Card
ORD-2026-9002,2,2026-03-25 11:00:00,DELIVERED,SKU-HOME-2001,1,79.95,PayPal
"""
    valid, rejected, summary = validate_and_transform_records(valid_csv)
    assert summary['total_rows_processed'] == 2
    assert summary['valid_records_count'] == 2
    assert summary['rejected_records_count'] == 0
    assert len(valid) == 2
    assert valid[0]['subtotal'] == 299.98
    assert valid[0]['tax_amount'] == 24.00
    assert valid[0]['shipping_fee'] == 0.00
    assert valid[0]['total_amount'] == 323.98


def test_lambda_validation_corrupted_rows():
    corrupted_csv = """order_number,customer_id,order_date,status,product_sku,quantity,unit_price,payment_method
ORD-9001,,2026-03-25,PENDING,SKU-1,1,10.00,Credit Card
ORD-9002,1,INVALID_DATE,PENDING,SKU-2,1,10.00,Credit Card
ORD-9003,1,2026-03-25,INVALID_STATUS,SKU-3,1,10.00,Credit Card
ORD-9004,1,2026-03-25,PENDING,SKU-4,-2,10.00,Credit Card
ORD-9005,1,2026-03-25,PENDING,SKU-5,0,10.00,Credit Card
"""
    valid, rejected, summary = validate_and_transform_records(corrupted_csv)
    assert summary['total_rows_processed'] == 5
    assert summary['valid_records_count'] == 0
    assert summary['rejected_records_count'] == 5


def test_lambda_handler_empty_event():
    resp = lambda_handler({})
    assert resp['statusCode'] == 400
