from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.database import db_session
from app.models import Order, Customer, Product, OrderItem

web_bp = Blueprint('web', __name__)

DEMO_USER = 'admin@retail.com'
DEMO_PASS = 'Admin123!'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('web.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@web_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('web.orders_page'))

    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if username == DEMO_USER and password == DEMO_PASS:
            session['logged_in'] = True
            session['user_email'] = username
            flash('Logged in successfully.', 'success')
            next_url = request.args.get('next') or url_for('web.orders_page')
            return redirect(next_url)
        else:
            error = 'Invalid email or password. Please try again.'

    return render_template('login.html', error=error)


@web_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('web.login'))


@web_bp.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('web.login'))
    return redirect(url_for('web.orders_page'))


@web_bp.route('/orders')
@login_required
def orders_page():
    status = request.args.get('status', '').strip()
    search = request.args.get('search', '').strip()
    start_date = request.args.get('start_date', '').strip()
    end_date = request.args.get('end_date', '').strip()

    query = db_session.query(Order).join(Customer)

    if status:
        query = query.filter(Order.status == status.upper())
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Order.order_number.ilike(search_term)) |
            (Customer.first_name.ilike(search_term)) |
            (Customer.last_name.ilike(search_term)) |
            (Customer.email.ilike(search_term)) |
            (Customer.city.ilike(search_term))
        )
    if start_date:
        query = query.filter(Order.order_date >= f"{start_date} 00:00:00")
    if end_date:
        query = query.filter(Order.order_date <= f"{end_date} 23:59:59")

    orders = query.order_by(Order.order_date.desc()).all()
    total_count = len(orders)
    
    return render_template(
        'orders.html', 
        orders=orders, 
        total_count=total_count,
        filter_status=status,
        filter_search=search,
        filter_start_date=start_date,
        filter_end_date=end_date
    )


@web_bp.route('/orders/<int:order_id>')
@login_required
def order_detail(order_id):
    order = db_session.query(Order).get(order_id)
    if not order:
        flash(f"Order #{order_id} not found.", 'danger')
        return redirect(url_for('web.orders_page'))
    
    return render_template('order_detail.html', order=order)


@web_bp.route('/orders/<int:order_id>/update-status', methods=['POST'])
@login_required
def update_status_form(order_id):
    order = db_session.query(Order).get(order_id)
    if not order:
        flash(f"Order #{order_id} not found.", 'danger')
        return redirect(url_for('web.orders_page'))

    new_status = request.form.get('status', '').strip().upper()
    from app.validation import validate_status_transition, ValidationError
    
    try:
        validated_status = validate_status_transition(order.status, new_status)
        order.status = validated_status
        db_session.commit()
        flash(f"Order {order.order_number} status updated to {validated_status}.", 'success')
    except ValidationError as e:
        flash(f"Status Update Failed: {e.message}", 'danger')

    return redirect(url_for('web.order_detail', order_id=order_id))


@web_bp.route('/create-order', methods=['GET', 'POST'])
@login_required
def create_order_page():
    customers = db_session.query(Customer).order_by(Customer.first_name).all()
    products = db_session.query(Product).order_by(Product.product_name).all()
    return render_template('create_order.html', customers=customers, products=products)


@web_bp.route('/analytics')
@login_required
def analytics_page():
    return render_template('analytics.html')
