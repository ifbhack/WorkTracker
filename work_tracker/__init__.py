def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key = 'admin'
    SESSION_TYPE = 'redis'