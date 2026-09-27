import json
import uuid

def test_create_customer_success(client):
    unique_email = f"user_{uuid.uuid4().hex[:6]}@example.com"
    payload = {
        'first_name': 'Samantha',
        'last_name': 'Jones',
        'email': unique_email,
        'phone': '212-555-9988',
        'city': 'New York',
        'state': 'NY'
    }
    response = client.post('/api/customers', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert 'customer' in data
    assert data['customer']['email'] == unique_email
    assert data['customer']['customer_id'] is not None


def test_create_customer_duplicate_email(client):
    payload = {
        'first_name': 'Alice',
        'last_name': 'Smith',
        'email': 'alice.smith@example.com',  # Seed email
        'city': 'New York',
        'state': 'NY'
    }
    response = client.post('/api/customers', json=payload)
    assert response.status_code == 409
    data = response.get_json()
    assert 'already exists' in data['error']


def test_get_customer_by_id(client):
    response = client.get('/api/customers/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['customer_id'] == 1
    assert data['first_name'] == 'Alice'


def test_get_customer_not_found(client):
    response = client.get('/api/customers/99999')
    assert response.status_code == 404
    data = response.get_json()
    assert 'not found' in data['error'].lower()


def test_list_customers(client):
    response = client.get('/api/customers')
    assert response.status_code == 200
    data = response.get_json()
    assert 'customers' in data
    assert data['total'] >= 8
