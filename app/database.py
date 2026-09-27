import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

Base = declarative_base()
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False))

def get_engine(db_url=None):
    if db_url is None:
        db_url = os.environ.get('DATABASE_URL', 'sqlite:///retail_orders.db')
    
    # Handle SQLite connect args for multi-threading
    if db_url.startswith('sqlite'):
        return create_engine(db_url, connect_args={'check_same_thread': False})
    return create_engine(db_url)

def init_db(app=None):
    db_url = app.config.get('DATABASE_URL') if app else os.environ.get('DATABASE_URL', 'sqlite:///retail_orders.db')
    engine = get_engine(db_url)
    db_session.configure(bind=engine)
    
    from app.models import Customer, Product, Order, OrderItem  # noqa: F401
    Base.metadata.create_all(bind=engine)
    
    if app:
        @app.teardown_appcontext
        def shutdown_session(exception=None):
            db_session.remove()
    return engine
