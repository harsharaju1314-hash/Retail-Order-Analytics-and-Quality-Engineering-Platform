import re
from datetime import datetime

VALID_ORDER_STATUSES = {'PENDING', 'CONFIRMED', 'SHIPPED', 'DELIVERED', 'CANCELLED'}
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

VALID_STATUS_TRANSITIONS = {
    'PENDING': {'CONFIRMED', 'CANCELLED'},
    'CONFIRMED': {'SHIPPED', 'CANCELLED'},
    'SHIPPED': {'DELIVERED'},
    'DELIVERED': set(),  # Terminal state
    'CANCELLED': set()   # Terminal state
}

class ValidationError(Exception):
    """Custom exception for business validation failures."""
    def __init__(self, message, field=None, status_code=400):
        super().__init__(message)
        self.message = message
        self.field = field
        self.status_code = status_code

    def to_dict(self):
        res = {'error': self.message}
        if self.field:
            res['field'] = self.field
        return res


def validate_customer_payload(data):
    """Validates customer creation payload."""
    if not isinstance(data, dict) or not data:
        raise ValidationError("Request body cannot be empty and must be a valid JSON object.", status_code=400)

    required_fields = ['first_name', 'last_name', 'email', 'city', 'state']
    for field in required_fields:
        val = data.get(field)
        if val is None or str(val).strip() == '':
            raise ValidationError(f"'{field}' is a required field and cannot be empty.", field=field, status_code=400)

    email = str(data.get('email')).strip()
    if not EMAIL_REGEX.match(email):
        raise ValidationError(f"Invalid email format: '{email}'.", field='email', status_code=400)

    return {
        'first_name': str(data['first_name']).strip(),
        'last_name': str(data['last_name']).strip(),
        'email': email.lower(),
        'phone': str(data.get('phone', '')).strip() or None,
        'city': str(data['city']).strip(),
        'state': str(data['state']).strip().upper(),
        'country': str(data.get('country', 'USA')).strip(),
        'postal_code': str(data.get('postal_code', '')).strip() or None
    }


def validate_order_payload(data):
    """Validates order creation payload."""
    if not isinstance(data, dict) or not data:
        raise ValidationError("Request body cannot be empty and must be a valid JSON object.", status_code=400)

    customer_id = data.get('customer_id')
    if customer_id is None:
        raise ValidationError("'customer_id' is required.", field='customer_id', status_code=400)
    
    try:
        customer_id = int(customer_id)
        if customer_id <= 0:
            raise ValueError()
    except (ValueError, TypeError):
        raise ValidationError("'customer_id' must be a positive integer.", field='customer_id', status_code=400)

    items = data.get('items')
    if not isinstance(items, list) or len(items) == 0:
        raise ValidationError("An order must contain at least one item in the 'items' list.", field='items', status_code=400)

    validated_items = []
    seen_products = set()

    for idx, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValidationError(f"Item at index {idx} must be a JSON object.", field=f'items[{idx}]', status_code=400)

        product_id = item.get('product_id')
        if product_id is None:
            raise ValidationError(f"Item at index {idx} is missing 'product_id'.", field=f'items[{idx}].product_id', status_code=400)
        
        try:
            product_id = int(product_id)
            if product_id <= 0:
                raise ValueError()
        except (ValueError, TypeError):
            raise ValidationError(f"Item at index {idx} 'product_id' must be a positive integer.", field=f'items[{idx}].product_id', status_code=400)

        if product_id in seen_products:
            raise ValidationError(f"Duplicate product_id {product_id} in items list. Combine quantity into a single line item.", field=f'items[{idx}].product_id', status_code=400)
        seen_products.add(product_id)

        quantity = item.get('quantity')
        if quantity is None:
            raise ValidationError(f"Item at index {idx} is missing 'quantity'.", field=f'items[{idx}].quantity', status_code=400)
        
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError()
        except (ValueError, TypeError):
            raise ValidationError(f"Item at index {idx} 'quantity' must be an integer greater than 0.", field=f'items[{idx}].quantity', status_code=400)

        validated_items.append({
            'product_id': product_id,
            'quantity': quantity
        })

    payment_method = str(data.get('payment_method', 'Credit Card')).strip()
    shipping_address = str(data.get('shipping_address', '')).strip() or None
    order_number = str(data.get('order_number', '')).strip() or None

    return {
        'customer_id': customer_id,
        'items': validated_items,
        'order_number': order_number,
        'payment_method': payment_method,
        'shipping_address': shipping_address
    }


def validate_status_transition(current_status, new_status):
    """Validates order status transition."""
    if not new_status or not isinstance(new_status, str):
        raise ValidationError("Status is required and must be a string.", field='status', status_code=400)

    new_status = new_status.strip().upper()
    if new_status not in VALID_ORDER_STATUSES:
        raise ValidationError(f"Invalid status '{new_status}'. Allowed values: {sorted(list(VALID_ORDER_STATUSES))}", field='status', status_code=400)

    if current_status == new_status:
        return new_status

    allowed_transitions = VALID_STATUS_TRANSITIONS.get(current_status, set())
    if new_status not in allowed_transitions:
        raise ValidationError(f"Invalid status transition from '{current_status}' to '{new_status}'.", field='status', status_code=400)

    return new_status


def validate_date_string(date_str, field_name='date'):
    """Validates ISO/standard date string YYYY-MM-DD or YYYY-MM-DD HH:MM:SS."""
    if not date_str:
        return None
    for fmt in ('%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S'):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValidationError(f"Invalid date format for '{field_name}'. Expected YYYY-MM-DD.", field=field_name, status_code=400)
