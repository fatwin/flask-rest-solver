import logging
import os
from flask import Flask, jsonify, make_response, request
from api import api_bp

file_dir, file_name = os.path.split(os.path.abspath(__file__))
file_handler = logging.FileHandler(os.path.join(file_dir, 'app.log'))
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(filename)s %(lineno)d - %(levelname)s: %(message)s'))

app = Flask(__name__)

app_logger = app.logger
app_logger.addHandler(file_handler)
app_logger.setLevel(logging.INFO)

app.register_blueprint(api_bp, url_prefix='/api/v1.0')


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url
    }
    return jsonify(message), 404


@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
