from flask import Flask, request, jsonify
from controller.main import ShadowController
from core.settings import Settings

app = Flask(__name__)

@app.route('/scan', methods=['POST'])
def scan():
    data = request.json
    # Mock settings from JSON
    settings = Settings(type('Args', (), data))
    # controller = ShadowController(settings, session)
    # result = controller.run()
    return jsonify({"status": "scan initiated"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)