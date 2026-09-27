import json

def test_create_order_success(client):
    payload = {
        'customer_id': 1,
        'payment_method': 'Credit Card',
        'shipping_address': '100 Main St, New York, NY 10001',
        'items': [
            {'product_id': 1, 'quantity': 1},  # $149.99
            {'product_id': 2, 'quantity': 1}   # $89.50
        ]
    }
    response = client.post('/api/orders', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    order = data['order']
    assert order['status'] == 'PENDING'
    assert order['subtotal'] == 239.49
    assert order['tax_amount'] == 19.16
    assert order['shipping_fee'] == 0.00  # >= $100
    assert order['total_amount'] == 258.65
    assert len(order['items']) == 2


def test_create_order_with_shipping_fee(client):
    payload = {
        'customer_id': 2,
        'payment_method': 'Debit Card',
        'items': [
            {'product_id': 4, 'quantity': 1}  # $79.95 (< $100 -> shipping $10.00)
        ]
    }
    response = client.post('/api/orders', json=payload)
    assert response.status_code == 201
    order = response.get_json()['order']
    assert order['subtotal'] == 79.95
    assert order['shipping_fee'] == 10.00
    assert abs(order['total_amount'] - (79.95 + 6.40 + 10.00)) < 0.01


def test_get_order_by_id(client):
    response = client.get('/api/orders/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['order_id'] == 1
    assert 'items' in data
    assert len(data['items']) > 0


def test_get_order_not_found(client):
    response = client.get('/api/orders/99999')
    assert response.status_code == 404


def test_update_order_status_valid(client):
    # Update Order 5 (PENDING -> CONFIRMED)
    response = client.put('/api/orders/5/status', json={'status': 'CONFIRMED'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['order']['status'] == 'CONFIRMED'


def test_update_order_status_invalid_transition(client):
    # Try transitioning DELIVERED (Order 1) to PENDING
    response = client.put('/api/orders/1/status', json={'status': 'PENDING'})
    assert response.status_code == 400
    data = response.get_json()
    assert 'Invalid status transition' in data['error']


def test_list_orders_with_status_filter(client):
    response = client.get('/api/orders?status=DELIVERED')
    assert response.status_code == 200
    data = response.get_json()
    assert data['total'] >= 1
    for o in data['orders']:
        assert o['status'] == 'DELIVERED'


def test_list_orders_with_search(client):
    response = client.get('/api/orders?search=Alice')
    assert response.status_code == 200
    data = response.get_json()
    assert data['total'] >= 1


def test_analytics_summary_endpoint(client):
    response = client.get('/api/analytics/summary')
    assert response.status_code == 200
    data = response.get_json()
    assert 'kpis' in data
    assert data['kpis']['total_orders'] >= 10
    assert data['kpis']['total_revenue'] > 0
