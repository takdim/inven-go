from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from app import create_app

app = create_app()

if __name__ == '__main__':
    # host='0.0.0.0' agar bisa diakses dari jaringan WiFi yang sama
    # Akses dari perangkat lain: http://<IP_MAC_ANDA>:8000
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 8000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    app.run(host=host, port=port, debug=debug)
