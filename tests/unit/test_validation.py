import pytest
from app.validation import (
    ValidationError,
    validate_customer_payload,
    validate_order_payload,
    validate_status_transition,
    validate_date_string
)

def test_validate_customer_payload_success():
    payload = {
        'first_name': '  John ',
        'last_name': 'Doe  ',
        'email': '  John.Doe@Example.com ',
        'city': 'Chicago',
        'state': 'il'
    }
    validated = validate_customer_payload(payload)
    assert validated['first_name'] == 'John'
    assert validated['last_name'] == 'Doe'
    assert validated['email'] == 'john.doe@example.com'
    assert validated['state'] == 'IL'


def test_validate_customer_missing_field():
    with pytest.raises(ValidationError) as exc:
        validate_customer_payload({'first_name': 'John', 'email': 'john@test.com'})
    assert 'last_name' in exc.value.message


def test_validate_customer_invalid_email():
    with pytest.raises(ValidationError) as exc:
        validate_customer_payload({
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'invalid-email-address',
            'city': 'Dallas',
            'state': 'TX'
        })
    assert 'Invalid email format' in exc.value.message


def test_validate_order_payload_success():
    payload = {
        'customer_id': 1,
        'items': [
            {'product_id': 1, 'quantity': 2},
            {'product_id': 2, 'quantity': 1}
        ]
    }
    validated = validate_order_payload(payload)
    assert validated['customer_id'] == 1
    assert len(validated['items']) == 2
    assert validated['items'][0]['quantity'] == 2


def test_validate_order_zero_quantity():
    payload = {
        'customer_id': 1,
        'items': [{'product_id': 1, 'quantity': 0}]
    }
    with pytest.raises(ValidationError) as exc:
        validate_order_payload(payload)
    assert 'greater than 0' in exc.value.message


def test_validate_order_duplicate_product_id():
    payload = {
        'customer_id': 1,
        'items': [
            {'product_id': 1, 'quantity': 1},
            {'product_id': 1, 'quantity': 2}
        ]
    }
    with pytest.raises(ValidationError) as exc:
        validate_order_payload(payload)
    assert 'Duplicate product_id' in exc.value.message


def test_status_transitions_valid():
    assert validate_status_transition('PENDING', 'CONFIRMED') == 'CONFIRMED'
    assert validate_status_transition('CONFIRMED', 'SHIPPED') == 'SHIPPED'
    assert validate_status_transition('SHIPPED', 'DELIVERED') == 'DELIVERED'
    assert validate_status_transition('PENDING', 'CANCELLED') == 'CANCELLED'


def test_status_transitions_invalid():
    with pytest.raises(ValidationError) as exc:
        validate_status_transition('DELIVERED', 'PENDING')
    assert 'Invalid status transition' in exc.value.message

    with pytest.raises(ValidationError) as exc:
        validate_status_transition('CANCELLED', 'SHIPPED')
    assert 'Invalid status transition' in exc.value.message


def test_date_validation():
    dt = validate_date_string('2026-03-25')
    assert dt.year == 2026 and dt.month == 3 and dt.day == 25

    with pytest.raises(ValidationError) as exc:
        validate_date_string('25/03/2026')
    assert 'Invalid date format' in exc.value.message
