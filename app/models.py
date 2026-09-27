from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Customer(Base):
    __tablename__ = 'customers'

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), nullable=True)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    country = Column(String(50), default='USA')
    postal_code = Column(String(20), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    orders = relationship('Order', back_populates='customer', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'customer_id': self.customer_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': f"{self.first_name} {self.last_name}",
            'email': self.email,
            'phone': self.phone,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'postal_code': self.postal_code,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }


class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    sku = Column(String(30), unique=True, nullable=False)
    product_name = Column(String(150), nullable=False)
    category = Column(String(50), nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    stock_quantity = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    order_items = relationship('OrderItem', back_populates='product')

    def to_dict(self):
        return {
            'product_id': self.product_id,
            'sku': self.sku,
            'product_name': self.product_name,
            'category': self.category,
            'unit_price': float(self.unit_price) if self.unit_price is not None else 0.0,
            'stock_quantity': self.stock_quantity,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }


class Order(Base):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True, autoincrement=True)
    order_number = Column(String(50), unique=True, nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.customer_id', ondelete='RESTRICT'), nullable=False)
    order_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    status = Column(String(20), nullable=False, default='PENDING')
    subtotal = Column(Numeric(10, 2), nullable=False, default=0.00)
    tax_amount = Column(Numeric(10, 2), nullable=False, default=0.00)
    shipping_fee = Column(Numeric(10, 2), nullable=False, default=0.00)
    total_amount = Column(Numeric(10, 2), nullable=False, default=0.00)
    payment_method = Column(String(30), default='Credit Card')
    shipping_address = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    customer = relationship('Customer', back_populates='orders')
    items = relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')

    def to_dict(self, include_items=True):
        data = {
            'order_id': self.order_id,
            'order_number': self.order_number,
            'customer_id': self.customer_id,
            'customer_name': f"{self.customer.first_name} {self.customer.last_name}" if self.customer else None,
            'customer_email': self.customer.email if self.customer else None,
            'customer_city': self.customer.city if self.customer else None,
            'customer_state': self.customer.state if self.customer else None,
            'order_date': self.order_date.strftime('%Y-%m-%d %H:%M:%S') if self.order_date else None,
            'status': self.status,
            'subtotal': float(self.subtotal) if self.subtotal is not None else 0.0,
            'tax_amount': float(self.tax_amount) if self.tax_amount is not None else 0.0,
            'shipping_fee': float(self.shipping_fee) if self.shipping_fee is not None else 0.0,
            'total_amount': float(self.total_amount) if self.total_amount is not None else 0.0,
            'payment_method': self.payment_method,
            'shipping_address': self.shipping_address,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }
        if include_items and self.items:
            data['items'] = [item.to_dict() for item in self.items]
            data['item_count'] = sum(item.quantity for item in self.items)
        else:
            data['items'] = []
            data['item_count'] = 0
        return data


class OrderItem(Base):
    __tablename__ = 'order_items'

    item_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.order_id', ondelete='CASCADE'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.product_id', ondelete='RESTRICT'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    item_total = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    order = relationship('Order', back_populates='items')
    product = relationship('Product', back_populates='order_items')

    def to_dict(self):
        return {
            'item_id': self.item_id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'product_name': self.product.product_name if self.product else None,
            'product_sku': self.product.sku if self.product else None,
            'product_category': self.product.category if self.product else None,
            'quantity': self.quantity,
            'unit_price': float(self.unit_price) if self.unit_price is not None else 0.0,
            'item_total': float(self.item_total) if self.item_total is not None else 0.0
        }
