import os
import sys
import pytest
import threading
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.database import Base, get_engine, db_session
from app.models import Customer, Product, Order, OrderItem
from scripts.init_db import seed_database
import socket

@pytest.fixture(scope='session')
def app():
    # Use SQLite for reliable, self-contained test execution
    db_path = os.path.abspath('test_retail.db')
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except OSError:
            pass

    test_config = {
        'TESTING': True,
        'DATABASE_URL': f'sqlite:///{db_path}',
        'SECRET_KEY': 'test-secret-key'
    }

    app_instance = create_app(test_config)
    with app_instance.app_context():
        seed_database()
        yield app_instance

    # Teardown
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except OSError:
            pass


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


def get_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port


@pytest.fixture(scope='session')
def live_server_url(app):
    """Starts a live Flask server thread for Playwright UI tests."""
    port = get_free_port()
    
    server = threading.Thread(
        target=lambda: app.run(host='127.0.0.1', port=port, debug=False, use_reloader=False),
        daemon=True
    )
    server.start()
    
    # Wait for server to boot
    time.sleep(1.0)
    return f"http://127.0.0.1:{port}"
