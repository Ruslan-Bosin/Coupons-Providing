from flask import Flask
from loguru import logger
from config import LOG_NAME, LOG_ROTATION

# Создание основного web приложения
app: Flask = Flask(__name__)

# Добавление файла сохранения log-ов
logger.add(
    sink=LOG_NAME,
    level="DEBUG",
    rotation=LOG_ROTATION,
    compression="zip",
)

# Подключение отслеживания URL
from app import routes
