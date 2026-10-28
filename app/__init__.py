from flask import Flask

app = Flask(__name__)
app.secret_key = 'my_secret_key_lab4'

from . import views

from .users import users_bp
app.register_blueprint(users_bp)

from .products import products_bp
app.register_blueprint(products_bp)