from flask import Flask, send_from_directory
import os

# Flask uygulaması
app = Flask(__name__, static_folder='static')

# Ana sayfa olarak index.html'yi sun
@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

# Uygulama sunucusu
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Render gibi servisler portu dışarıdan verir
    app.run(host='0.0.0.0', port=port)
