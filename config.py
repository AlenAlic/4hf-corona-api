import os
import json
# noinspection PyPackageRequirements
from dotenv import load_dotenv
from constants import WORKERS

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config(object):

    ENV = os.environ.get("ENV") or "production"
    DEBUG = os.environ.get("DEBUG") == "True" or False

    SECRET_KEY = os.environ.get("SECRET_KEY") or "secret-key"
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_HOST = os.environ.get("DB_HOST") or "localhost"
    DB_PORT = os.environ.get("DB_PORT") or 3306
    DB_NAME = os.environ.get("DB_NAME")
    DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4" \
        if DB_USER and DB_PASSWORD and DB_NAME else None
    SQLALCHEMY_DATABASE_URI = DATABASE_URI or "sqlite:///" + os.path.join(basedir, "app.db")

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = False

    MAIL_SERVER = os.environ.get("MAIL_SERVER") or "localhost"
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 8025)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") or ""
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME") or ""
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD") or ""
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER") or "email@example.com"

    ERROR_EMAIL = os.environ.get("ERROR_EMAIL") or "error@example.com"

    FLASK_ADMIN_FLUID_LAYOUT = True
    FLASK_ADMIN_SWATCH = "flatly"

    PRETTY_URL = os.environ.get("PRETTY_URL") or "example.com"
    BASE_URL = "https://" + PRETTY_URL
    ACTIVATE_URL = BASE_URL + "/activate/"
    RESET_URL = BASE_URL + "/password/reset/"

    allowed_urls = os.environ.get("ALLOWED_URLS")
    ALLOWED_URLS = json.loads(allowed_urls) if allowed_urls else ["http://127.0.0.1:8080", "http://localhost:8080"]

    PUSH_PRIVATE_KEY = os.environ.get("PUSH_PRIVATE_KEY") or "push_private_key"
    PUSH_PUBLIC_KEY = os.environ.get("PUSH_PUBLIC_KEY") or "push_public_key"
    PUSH_EMAIL = os.environ.get("PUSH_EMAIL") or "push@example.com"

    REDIS_HOST = os.environ.get("REDIS_HOST") or "127.0.0.1"
    REDIS_PORT = os.environ.get("REDIS_PORT") or "6379"

    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

    RQ_WORKERS = WORKERS
