import pytest
from app.database import db_session
from app.models import Order, Product, OrderItem
from sqlalchemy import func

def test_reconciliation_total_orders_and_items(app):
    with app.app_context():
        # Source of truth query
        total_orders = db_session.query(func.count(Order.order_id)).scalar()
        orders_with_items = db_session.query(func.count(func.distinct(OrderItem.order_id))).scalar()
        
        # Every order must have associated order line items
        assert total_orders > 0, "No orders found in database."
        assert total_orders == orders_with_items, f"Discrepancy: {total_orders} orders but {orders_with_items} have items."


def test_reconciliation_net_revenue_formula(app):
    with app.app_context():
        # Gross vs Net Revenue Reconciliation
        gross_revenue = db_session.query(func.sum(Order.total_amount)).scalar() or 0.0
        cancelled_revenue = db_session.query(func.sum(Order.total_amount))\
            .filter(Order.status == 'CANCELLED').scalar() or 0.0
        net_revenue = db_session.query(func.sum(Order.total_amount))\
            .filter(Order.status != 'CANCELLED').scalar() or 0.0

        # Math reconciliation
        calculated_net = float(gross_revenue) - float(cancelled_revenue)
        assert abs(float(net_revenue) - calculated_net) < 0.01, "Financial reconciliation formula mismatch!"


def test_reconciliation_status_distribution_sum(app):
    with app.app_context():
        total_orders = db_session.query(func.count(Order.order_id)).scalar()
        status_counts = db_session.query(Order.status, func.count(Order.order_id)).group_by(Order.status).all()
        summed_by_status = sum(c[1] for c in status_counts)
        
        assert total_orders == summed_by_status, "Status breakdown does not sum to total order count."
