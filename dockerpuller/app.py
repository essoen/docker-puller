from flask import Flask
from flask import request
from flask import jsonify
import json
import subprocess

app = Flask(__name__)
config = None

@app.route('/dockerhook', methods=['POST'])
def hook_listen():
    if request.method != 'POST':
        return jsonify(success=False, error="Invalid request method"), 400

    token = request.args.get('token')
    if token != config['token']:
        return jsonify(success=False, error="Invalid token"), 400

    hook = request.args.get('hook')
    if not hook:
        return jsonify(success=False, error="Invalid request: missing hook"), 400
    hook_value = config['hooks'].get(hook)

    if hook_value:
        try:
            subprocess.call(hook_value)
            return jsonify(success=True), 200
        except OSError as e:
            return jsonify(success=False, error=str(e)), 400
    else:
        return jsonify(success=False, error="Hook not found"), 404

def load_config():
    with open('config.json') as config_file:    
        return json.load(config_file)

if __name__ == '__main__':
    config = load_config()
    app.run(host=config.get('host', 'localhost'), port=config.get('port', 8000))
