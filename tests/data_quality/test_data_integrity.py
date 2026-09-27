import pytest
from app.database import db_session
from app.models import Customer, Product, Order, OrderItem
from sqlalchemy import func

def test_dq_completeness_customers(app):
    with app.app_context():
        # Check mandatory customer fields
        null_customers = db_session.query(Customer).filter(
            (Customer.first_name == None) | (Customer.last_name == None) | (Customer.email == None)
        ).count()
        assert null_customers == 0, "Completeness violation: Found customers with NULL mandatory fields."


def test_dq_completeness_orders(app):
    with app.app_context():
        null_orders = db_session.query(Order).filter(
            (Order.order_number == None) | (Order.customer_id == None) | (Order.status == None) | (Order.total_amount == None)
        ).count()
        assert null_orders == 0, "Completeness violation: Found orders with NULL mandatory fields."


def test_dq_accuracy_order_totals(app):
    with app.app_context():
        orders = db_session.query(Order).all()
        for ord_obj in orders:
            items_sum = sum(float(item.item_total) for item in ord_obj.items)
            assert abs(float(ord_obj.subtotal) - items_sum) < 0.01, f"Accuracy discrepancy on Order #{ord_obj.order_id}"
            
            calculated_total = float(ord_obj.subtotal) + float(ord_obj.tax_amount) + float(ord_obj.shipping_fee)
            assert abs(float(ord_obj.total_amount) - calculated_total) < 0.01, f"Total formula discrepancy on Order #{ord_obj.order_id}"


def test_dq_consistency_foreign_keys(app):
    with app.app_context():
        # Check for orphan order items
        all_order_ids = {o.order_id for o in db_session.query(Order.order_id).all()}
        all_product_ids = {p.product_id for p in db_session.query(Product.product_id).all()}

        order_items = db_session.query(OrderItem).all()
        for item in order_items:
            assert item.order_id in all_order_ids, f"Consistency failure: Orphan item {item.item_id}"
            assert item.product_id in all_product_ids, f"Consistency failure: Non-existent product in item {item.item_id}"


def test_dq_uniqueness_orders(app):
    with app.app_context():
        duplicate_orders = db_session.query(Order.order_number, func.count(Order.order_id))\
            .group_by(Order.order_number)\
            .having(func.count(Order.order_id) > 1)\
            .all()
        assert len(duplicate_orders) == 0, f"Uniqueness violation: Found duplicate order numbers: {duplicate_orders}"


def test_dq_validity_status_and_quantities(app):
    with app.app_context():
        valid_statuses = {'PENDING', 'CONFIRMED', 'SHIPPED', 'DELIVERED', 'CANCELLED'}
        orders = db_session.query(Order).all()
        for ord_obj in orders:
            assert ord_obj.status in valid_statuses, f"Validity violation: Invalid status {ord_obj.status}"

        items = db_session.query(OrderItem).all()
        for item in items:
            assert item.quantity > 0, f"Validity violation: Non-positive quantity on item {item.item_id}"
            assert float(item.unit_price) >= 0.0, f"Validity violation: Negative price on item {item.item_id}"
