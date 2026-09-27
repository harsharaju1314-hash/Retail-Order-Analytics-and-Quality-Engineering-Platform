import json

def test_create_order_empty_payload(client):
    response = client.post('/api/orders', json={})
    assert response.status_code == 400
    assert 'empty' in response.get_json()['error'].lower()


def test_create_order_invalid_customer_id(client):
    response = client.post('/api/orders', json={
        'customer_id': 99999,
        'items': [{'product_id': 1, 'quantity': 1}]
    })
    assert response.status_code == 404
    assert 'Customer with ID 99999 not found' in response.get_json()['error']


def test_create_order_invalid_product_id(client):
    response = client.post('/api/orders', json={
        'customer_id': 1,
        'items': [{'product_id': 99999, 'quantity': 1}]
    })
    assert response.status_code == 404
    assert 'Product with ID 99999 not found' in response.get_json()['error']


def test_create_order_invalid_quantity_negative(client):
    response = client.post('/api/orders', json={
        'customer_id': 1,
        'items': [{'product_id': 1, 'quantity': -4}]
    })
    assert response.status_code == 400
    assert 'greater than 0' in response.get_json()['error']


def test_update_status_non_existent_order(client):
    response = client.put('/api/orders/99999/status', json={'status': 'CONFIRMED'})
    assert response.status_code == 404


def test_list_orders_invalid_page(client):
    response = client.get('/api/orders?page=0')
    assert response.status_code == 400
    assert 'page' in response.get_json()['error']
