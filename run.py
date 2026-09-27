import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() in ('true', '1', 't')
    print(f"Starting Retail Order Platform on http://127.0.0.1:{port}")
    app.run(host='127.0.0.1', port=port, debug=debug)
