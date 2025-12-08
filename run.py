from app import create_app

app = create_app()

if __name__ == '__main__':
    # host='0.0.0.0' agar bisa diakses dari jaringan WiFi yang sama
    # Akses dari perangkat lain: http://<IP_MAC_ANDA>:8000
    app.run(host='0.0.0.0', port=8000, debug=True)
