from flask import Flask

app = Flask(__name__)
app.secret_key = 'my_secret_key_lab4'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

from . import views

from .users import users_bp
app.register_blueprint(users_bp)

from .products import products_bp
app.register_blueprint(products_bp)