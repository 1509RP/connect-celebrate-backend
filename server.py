from flask import Flask, send_from_directory
from flask_cors import CORS
from api_routes import api
from config import Config
import os

app = Flask(__name__, static_folder='.')
app.config.from_object(Config)
CORS(app)

app.register_blueprint(api)

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(path):
        return send_from_directory('.', path)
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
