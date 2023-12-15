from flask import Flask
from api import api_blueprint
import flask_cors

app = Flask(__name__)
flask_cors.CORS(app)
app.register_blueprint(api_blueprint, url_prefix='/api')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)