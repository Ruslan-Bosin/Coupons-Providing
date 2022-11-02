from app import app, logger


# Отслеживание URL
@app.route("/")
def index() -> str:
    return "Index page"


# Отслеживание ошибок
@app.errorhandler(404)
def page_not_found_error(error_message):
    logger.info(error_message)
    return "404 Error", 404
