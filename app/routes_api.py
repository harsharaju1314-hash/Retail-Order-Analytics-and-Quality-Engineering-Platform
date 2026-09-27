import uuid
from datetime import datetime
from decimal import Decimal
from flask import Blueprint, request, jsonify
from sqlalchemy import func, or_
from app.database import db_session
from app.models import Customer, Product, Order, OrderItem
from app.validation import (
    ValidationError, 
    validate_customer_payload, 
    validate_order_payload, 
    validate_status_transition, 
    validate_date_string
)

api_bp = Blueprint('api', __name__)

@api_bp.errorhandler(ValidationError)
def handle_validation_error(err):
    return jsonify(err.to_dict()), err.status_code

@api_bp.errorhandler(404)
def handle_404_error(err):
    return jsonify({'error': 'Resource not found'}), 404

@api_bp.errorhandler(500)
def handle_500_error(err):
    return jsonify({'error': 'Internal server error'}), 500


# -----------------------------------------------------------------------------
# Customer APIs
# -----------------------------------------------------------------------------
@api_bp.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json(silent=True)
    if data is None:
        raise ValidationError("Empty or malformed JSON payload.", status_code=400)
    
    validated = validate_customer_payload(data)

    existing = db_session.query(Customer).filter_by(email=validated['email']).first()
    if existing:
        return jsonify({
            'error': f"Customer with email '{validated['email']}' already exists.",
            'field': 'email'
        }), 409

    customer = Customer(**validated)
    db_session.add(customer)
    db_session.commit()

    return jsonify({
        'message': 'Customer created successfully',
        'customer': customer.to_dict()
    }), 201


@api_bp.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = db_session.query(Customer).get(customer_id)
    if not customer:
        return jsonify({'error': f"Customer with ID {customer_id} not found."}), 404
    return jsonify(customer.to_dict()), 200


@api_bp.route('/customers', methods=['GET'])
def list_customers():
    customers = db_session.query(Customer).order_by(Customer.customer_id.asc()).all()
    return jsonify({
        'total': len(customers),
        'customers': [c.to_dict() for c in customers]
    }), 200


# -----------------------------------------------------------------------------
# Product APIs
# -----------------------------------------------------------------------------
@api_bp.route('/products', methods=['GET'])
def list_products():
    category = request.args.get('category')
    query = db_session.query(Product)
    if category:
        query = query.filter(Product.category.ilike(category.strip()))
    
    products = query.order_by(Product.product_id.asc()).all()
    return jsonify({
        'total': len(products),
        'products': [p.to_dict() for p in products]
    }), 200


# -----------------------------------------------------------------------------
# Order APIs
# -----------------------------------------------------------------------------
@api_bp.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json(silent=True)
    if data is None:
        raise ValidationError("Empty or malformed JSON payload.", status_code=400)

    validated = validate_order_payload(data)

    # 1. Verify customer exists
    customer = db_session.query(Customer).get(validated['customer_id'])
    if not customer:
        return jsonify({'error': f"Customer with ID {validated['customer_id']} not found."}), 404

    # 2. Verify order_number uniqueness if provided
    order_number = validated['order_number']
    if order_number:
        existing_order = db_session.query(Order).filter_by(order_number=order_number).first()
        if existing_order:
            return jsonify({'error': f"Order number '{order_number}' already exists."}), 409
    else:
        # Generate standard order number
        order_number = f"ORD-{datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

    # 3. Fetch products and calculate line totals
    subtotal = Decimal('0.00')
    order_items_to_create = []

    for item_data in validated['items']:
        product = db_session.query(Product).get(item_data['product_id'])
        if not product:
            return jsonify({'error': f"Product with ID {item_data['product_id']} not found."}), 404

        qty = item_data['quantity']
        price = Decimal(str(product.unit_price))
        item_total = price * Decimal(qty)
        subtotal += item_total

        order_items_to_create.append({
            'product_id': product.product_id,
            'quantity': qty,
            'unit_price': price,
            'item_total': item_total
        })

    # Standard Tax (8%) and Shipping ($10.00 if subtotal < $100 else Free)
    tax_rate = Decimal('0.08')
    tax_amount = (subtotal * tax_rate).quantize(Decimal('0.01'))
    shipping_fee = Decimal('10.00') if subtotal < Decimal('100.00') else Decimal('0.00')
    total_amount = subtotal + tax_amount + shipping_fee

    # Create Order
    new_order = Order(
        order_number=order_number,
        customer_id=customer.customer_id,
        order_date=datetime.utcnow(),
        status='PENDING',
        subtotal=subtotal,
        tax_amount=tax_amount,
        shipping_fee=shipping_fee,
        total_amount=total_amount,
        payment_method=validated['payment_method'],
        shipping_address=validated['shipping_address'] or f"{customer.city}, {customer.state} {customer.postal_code or ''}".strip()
    )
    db_session.add(new_order)
    db_session.flush()

    # Create Order Items
    for oi in order_items_to_create:
        item_record = OrderItem(
            order_id=new_order.order_id,
            product_id=oi['product_id'],
            quantity=oi['quantity'],
            unit_price=oi['unit_price'],
            item_total=oi['item_total']
        )
        db_session.add(item_record)

    db_session.commit()

    return jsonify({
        'message': 'Order created successfully',
        'order': new_order.to_dict(include_items=True)
    }), 201


@api_bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = db_session.query(Order).get(order_id)
    if not order:
        return jsonify({'error': f"Order with ID {order_id} not found."}), 404
    return jsonify(order.to_dict(include_items=True)), 200


@api_bp.route('/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    order = db_session.query(Order).get(order_id)
    if not order:
        return jsonify({'error': f"Order with ID {order_id} not found."}), 404

    data = request.get_json(silent=True)
    if data is None or not isinstance(data, dict):
        raise ValidationError("Empty or malformed JSON payload.", status_code=400)

    new_status = data.get('status')
    validated_status = validate_status_transition(order.status, new_status)

    order.status = validated_status
    order.updated_at = datetime.utcnow()
    db_session.commit()

    return jsonify({
        'message': f"Order status updated to '{validated_status}' successfully.",
        'order': order.to_dict(include_items=True)
    }), 200


@api_bp.route('/orders', methods=['GET'])
def list_orders():
    status = request.args.get('status')
    customer_id = request.args.get('customer_id')
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    search = request.args.get('search')
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)

    if page < 1:
        raise ValidationError("'page' must be greater than or equal to 1.", field='page', status_code=400)
    if page_size < 1 or page_size > 100:
        raise ValidationError("'page_size' must be between 1 and 100.", field='page_size', status_code=400)

    query = db_session.query(Order).join(Customer)

    if status:
        status_clean = status.strip().upper()
        if status_clean not in {'PENDING', 'CONFIRMED', 'SHIPPED', 'DELIVERED', 'CANCELLED'}:
            raise ValidationError(f"Invalid status filter '{status}'.", field='status', status_code=400)
        query = query.filter(Order.status == status_clean)

    if customer_id:
        try:
            cid = int(customer_id)
            query = query.filter(Order.customer_id == cid)
        except ValueError:
            raise ValidationError("'customer_id' filter must be an integer.", field='customer_id', status_code=400)

    if start_date_str:
        start_date = validate_date_string(start_date_str, 'start_date')
        query = query.filter(Order.order_date >= start_date)

    if end_date_str:
        end_date = validate_date_string(end_date_str, 'end_date')
        # Include entire end day
        end_date = end_date.replace(hour=23, minute=59, second=59)
        query = query.filter(Order.order_date <= end_date)

    if search:
        search_term = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Order.order_number.ilike(search_term),
                Customer.first_name.ilike(search_term),
                Customer.last_name.ilike(search_term),
                Customer.email.ilike(search_term),
                Customer.city.ilike(search_term)
            )
        )

    total_count = query.count()
    orders = query.order_by(Order.order_date.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return jsonify({
        'total': total_count,
        'page': page,
        'page_size': page_size,
        'orders': [o.to_dict(include_items=False) for o in orders]
    }), 200


# -----------------------------------------------------------------------------
# Analytics API Endpoint (Source of Truth Reconciliation)
# -----------------------------------------------------------------------------
@api_bp.route('/analytics/summary', methods=['GET'])
def analytics_summary():
    total_orders = db_session.query(func.count(Order.order_id)).scalar() or 0
    total_revenue = db_session.query(func.sum(Order.total_amount)).filter(Order.status != 'CANCELLED').scalar() or 0.0
    avg_order_value = (float(total_revenue) / total_orders) if total_orders > 0 else 0.0
    
    # Orders by status
    status_counts = db_session.query(Order.status, func.count(Order.order_id)).group_by(Order.status).all()
    status_dict = {s: c for s, c in status_counts}

    # Revenue by Category
    cat_data = db_session.query(
        Product.category,
        func.sum(OrderItem.item_total).label('category_revenue'),
        func.sum(OrderItem.quantity).label('units_sold')
    ).join(OrderItem, Product.product_id == OrderItem.product_id)\
     .join(Order, OrderItem.order_id == Order.order_id)\
     .filter(Order.status != 'CANCELLED')\
     .group_by(Product.category).all()

    category_summary = [
        {
            'category': c[0],
            'revenue': float(c[1]) if c[1] else 0.0,
            'units_sold': int(c[2]) if c[2] else 0
        }
        for c in cat_data
    ]

    return jsonify({
        'kpis': {
            'total_orders': total_orders,
            'total_revenue': round(float(total_revenue), 2),
            'avg_order_value': round(avg_order_value, 2)
        },
        'orders_by_status': status_dict,
        'revenue_by_category': category_summary
    }), 200
