from flask import Flask, render_template
from loguru import logger
from config import LOG_NAME, LOG_ROTATION, SECRET_KEY


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

# Подключение отслеживания URL
from app import routes
