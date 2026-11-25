import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate
from dotenv import load_dotenv
from sqlalchemy import MetaData

from .config import config_map

load_dotenv()

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })

db = SQLAlchemy(model_class=Base)
migrate = Migrate()

def create_app(config_name: str = None) -> Flask:
    if config_name is None:
        config_name = os.environ.get("FLASK_CONFIG", "dev")

    app = Flask(__name__)
    app.config.from_object(config_map[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    # Імпорт моделей для реєстрації в метаданих Alembic
    from .posts.models import Post
    from .users.models import User
    from app.products.models import Product

    # Реєстрація блюпринтів
    from .views import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .users import users_bp 
    app.register_blueprint(users_bp, url_prefix="/users")

    from .posts import post_bp
    app.register_blueprint(post_bp, url_prefix="/post")

    #from app.products.views import products_bp
    #app.register_blueprint(products_bp, url_prefix="/products")

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    return app