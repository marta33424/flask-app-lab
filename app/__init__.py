import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate
from dotenv import load_dotenv

from .config import config_map

load_dotenv()

class Base(DeclarativeBase):
    pass

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

    # Реєстрація блюпринтів
    from .views import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .users import users_bp 
    app.register_blueprint(users_bp, url_prefix="/users")

    from .posts import post_bp
    app.register_blueprint(post_bp, url_prefix="/post")

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    return app