from flask import Flask, render_template
from loguru import logger
from peewee import SqliteDatabase
from flask_login import LoginManager
from config import LOG_NAME, LOG_ROTATION, SECRET_KEY, DATABASE


# Создание основного web приложения
app: Flask = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY

# Добавление файла сохранения log-ов
logger.add(
    sink=LOG_NAME,
    level="DEBUG",
    rotation=LOG_ROTATION,
    compression="zip",
)

# Создание базы данных
db = SqliteDatabase(DATABASE)

# Настройка flask-login
login_manager = LoginManager(app=app)
login_manager.login_view = "select_role"
login_manager.login_message = ""

# Подключение отслеживания URL
from app import routes
from app.login import load_user
