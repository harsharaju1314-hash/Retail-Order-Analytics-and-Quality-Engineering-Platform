import os
import sys

# Ensure root directory is on path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import init_db, db_session
from app.models import Customer, Product, Order, OrderItem
from datetime import datetime
from decimal import Decimal

def seed_database(force_reset=False):
    """Initializes tables and populates realistic seed data."""
    init_db()

    if force_reset:
        print("Resetting database schema...")
        from app.database import Base, get_engine
        engine = get_engine()
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
    elif db_session.query(Customer).count() > 0:
        print("Database already contains data. Skipping seeding. Use --reset to re-seed.")
        return

    print("Seeding database with realistic retail records...")

    # Customers
    customers = [
        Customer(customer_id=1, first_name='Alice', last_name='Smith', email='alice.smith@example.com', phone='212-555-0101', city='New York', state='NY', country='USA', postal_code='10001', created_at=datetime(2026, 1, 10, 9, 0)),
        Customer(customer_id=2, first_name='Bob', last_name='Jones', email='bob.jones@example.com', phone='312-555-0102', city='Chicago', state='IL', country='USA', postal_code='60601', created_at=datetime(2026, 1, 12, 10, 15)),
        Customer(customer_id=3, first_name='Charlie', last_name='Brown', email='charlie.brown@example.com', phone='415-555-0103', city='San Francisco', state='CA', country='USA', postal_code='94105', created_at=datetime(2026, 1, 15, 11, 30)),
        Customer(customer_id=4, first_name='Diana', last_name='Prince', email='diana.prince@example.com', phone='206-555-0104', city='Seattle', state='WA', country='USA', postal_code='98101', created_at=datetime(2026, 1, 18, 14, 20)),
        Customer(customer_id=5, first_name='Evan', last_name='Wright', email='evan.wright@example.com', phone='512-555-0105', city='Austin', state='TX', country='USA', postal_code='78701', created_at=datetime(2026, 1, 20, 16, 45)),
        Customer(customer_id=6, first_name='Fiona', last_name='Gallagher', email='fiona.g@example.com', phone='617-555-0106', city='Boston', state='MA', country='USA', postal_code='02108', created_at=datetime(2026, 2, 1, 8, 30)),
        Customer(customer_id=7, first_name='George', last_name='Miller', email='george.m@example.com', phone='303-555-0107', city='Denver', state='CO', country='USA', postal_code='80202', created_at=datetime(2026, 2, 5, 13, 10)),
        Customer(customer_id=8, first_name='Hannah', last_name='Abbott', email='hannah.a@example.com', phone='404-555-0108', city='Atlanta', state='GA', country='USA', postal_code='30303', created_at=datetime(2026, 2, 10, 15, 0))
    ]
    db_session.add_all(customers)
    db_session.commit()

    # Products
    products = [
        Product(product_id=1, sku='SKU-ELEC-1001', product_name='Noise Cancelling Headphones', category='Electronics', unit_price=Decimal('149.99'), stock_quantity=50),
        Product(product_id=2, sku='SKU-ELEC-1002', product_name='Wireless Mechanical Keyboard', category='Electronics', unit_price=Decimal('89.50'), stock_quantity=80),
        Product(product_id=3, sku='SKU-ELEC-1003', product_name='Ultra HD Monitor 27-inch', category='Electronics', unit_price=Decimal('299.00'), stock_quantity=30),
        Product(product_id=4, sku='SKU-HOME-2001', product_name='Stainless Steel Coffee Maker', category='Home & Kitchen', unit_price=Decimal('79.95'), stock_quantity=45),
        Product(product_id=5, sku='SKU-HOME-2002', product_name='Non-Stick Ceramic Cookware Set', category='Home & Kitchen', unit_price=Decimal('129.00'), stock_quantity=40),
        Product(product_id=6, sku='SKU-APPR-3001', product_name='Classic Denim Jacket', category='Apparel', unit_price=Decimal('65.00'), stock_quantity=100),
        Product(product_id=7, sku='SKU-APPR-3002', product_name='Breathable Running Shoes', category='Apparel', unit_price=Decimal('85.00'), stock_quantity=60),
        Product(product_id=8, sku='SKU-SPRT-4001', product_name='Adjustable Dumbbell Set', category='Sports & Outdoors', unit_price=Decimal('199.50'), stock_quantity=25),
        Product(product_id=9, sku='SKU-SPRT-4002', product_name='Insulated Water Bottle 32oz', category='Sports & Outdoors', unit_price=Decimal('24.99'), stock_quantity=150),
        Product(product_id=10, sku='SKU-HOME-2003', product_name='Ergonomic Desk Chair', category='Home & Kitchen', unit_price=Decimal('185.00'), stock_quantity=35)
    ]
    db_session.add_all(products)
    db_session.commit()

    # Orders and Items
    orders_data = [
        {
            'order_id': 1, 'order_number': 'ORD-2026-0001', 'customer_id': 1, 'date': datetime(2026, 2, 15, 10, 30),
            'status': 'DELIVERED', 'shipping_fee': Decimal('10.00'), 'payment': 'Credit Card',
            'items': [(1, 1, Decimal('149.99')), (2, 1, Decimal('89.50'))]
        },
        {
            'order_id': 2, 'order_number': 'ORD-2026-0002', 'customer_id': 2, 'date': datetime(2026, 2, 16, 11, 45),
            'status': 'DELIVERED', 'shipping_fee': Decimal('15.00'), 'payment': 'Debit Card',
            'items': [(3, 1, Decimal('299.00'))]
        },
        {
            'order_id': 3, 'order_number': 'ORD-2026-0003', 'customer_id': 3, 'date': datetime(2026, 2, 18, 14, 15),
            'status': 'SHIPPED', 'shipping_fee': Decimal('10.00'), 'payment': 'Credit Card',
            'items': [(4, 1, Decimal('79.95')), (9, 2, Decimal('24.99'))]
        },
        {
            'order_id': 4, 'order_number': 'ORD-2026-0004', 'customer_id': 4, 'date': datetime(2026, 2, 20, 16, 0),
            'status': 'CONFIRMED', 'shipping_fee': Decimal('10.00'), 'payment': 'PayPal',
            'items': [(1, 1, Decimal('149.99')), (7, 1, Decimal('85.00'))]
        },
        {
            'order_id': 5, 'order_number': 'ORD-2026-0005', 'customer_id': 5, 'date': datetime(2026, 2, 22, 9, 10),
            'status': 'PENDING', 'shipping_fee': Decimal('15.00'), 'payment': 'Credit Card',
            'items': [(8, 1, Decimal('199.50'))]
        },
        {
            'order_id': 6, 'order_number': 'ORD-2026-0006', 'customer_id': 1, 'date': datetime(2026, 2, 25, 15, 30),
            'status': 'DELIVERED', 'shipping_fee': Decimal('5.00'), 'payment': 'Credit Card',
            'items': [(2, 1, Decimal('89.50'))]
        },
        {
            'order_id': 7, 'order_number': 'ORD-2026-0007', 'customer_id': 6, 'date': datetime(2026, 3, 1, 12, 0),
            'status': 'CANCELLED', 'shipping_fee': Decimal('10.00'), 'payment': 'Credit Card',
            'items': [(5, 1, Decimal('129.00'))]
        },
        {
            'order_id': 8, 'order_number': 'ORD-2026-0008', 'customer_id': 7, 'date': datetime(2026, 3, 5, 13, 40),
            'status': 'DELIVERED', 'shipping_fee': Decimal('15.00'), 'payment': 'Debit Card',
            'items': [(6, 1, Decimal('65.00')), (8, 1, Decimal('199.50'))]
        },
        {
            'order_id': 9, 'order_number': 'ORD-2026-0009', 'customer_id': 8, 'date': datetime(2026, 3, 10, 10, 20),
            'status': 'SHIPPED', 'shipping_fee': Decimal('15.00'), 'payment': 'PayPal',
            'items': [(10, 1, Decimal('185.00'))]
        },
        {
            'order_id': 10, 'order_number': 'ORD-2026-0010', 'customer_id': 3, 'date': datetime(2026, 3, 15, 16, 50),
            'status': 'CONFIRMED', 'shipping_fee': Decimal('20.00'), 'payment': 'Credit Card',
            'items': [(2, 1, Decimal('89.50')), (3, 1, Decimal('299.00'))]
        }
    ]

    for ord_info in orders_data:
        subtotal = Decimal('0.00')
        items_to_add = []
        for p_id, qty, price in ord_info['items']:
            line_total = price * Decimal(qty)
            subtotal += line_total
            items_to_add.append((p_id, qty, price, line_total))

        tax = (subtotal * Decimal('0.08')).quantize(Decimal('0.01'))
        total = subtotal + tax + ord_info['shipping_fee']

        ord_obj = Order(
            order_id=ord_info['order_id'],
            order_number=ord_info['order_number'],
            customer_id=ord_info['customer_id'],
            order_date=ord_info['date'],
            status=ord_info['status'],
            subtotal=subtotal,
            tax_amount=tax,
            shipping_fee=ord_info['shipping_fee'],
            total_amount=total,
            payment_method=ord_info['payment'],
            created_at=ord_info['date'],
            updated_at=ord_info['date']
        )
        db_session.add(ord_obj)
        db_session.flush()

        for p_id, qty, price, line_total in items_to_add:
            item_obj = OrderItem(
                order_id=ord_obj.order_id,
                product_id=p_id,
                quantity=qty,
                unit_price=price,
                item_total=line_total,
                created_at=ord_info['date']
            )
            db_session.add(item_obj)

    db_session.commit()
    print("Database successfully seeded!")

if __name__ == '__main__':
    force = '--reset' in sys.argv or '-r' in sys.argv
    seed_database(force_reset=force)
