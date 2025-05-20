from flask import Flask
from controllers import bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'auth_api_secret_key'

app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(port=5001, debug=True) 