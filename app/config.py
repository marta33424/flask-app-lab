import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))
root_dir = os.path.abspath(os.path.join(basedir, ".."))
instance_dir = os.path.join(root_dir, "instance")

os.makedirs(instance_dir, exist_ok=True)

class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    FLASK_DEBUG = 1
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URL",
        f"sqlite:///{os.path.join(instance_dir, 'data.sqlite')}"
    )

class TestingConfig(BaseConfig):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False

class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

config = {
    "dev": DevelopmentConfig,
    "development": DevelopmentConfig,
    "test": TestingConfig,
    "testing": TestingConfig,
    "prod": ProductionConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}

config_map = config