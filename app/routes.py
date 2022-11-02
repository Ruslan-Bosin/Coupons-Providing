from app import app, logger
from flask import render_template, url_for


# Отслеживание URL
# Ознакомительная страница
@app.route("/")
def index() -> str:
    data: [str, object] = {
        "title": "Главная страница",
        "select_role_url": url_for("select_role")
    }
    return render_template("index.html", **data)


# Выбор роли: клиент / организация
@app.route("/select_role")
def select_role() -> str:
    data: [str, object] = {
        "title": "Выберите кто вы",
        "index_url": url_for("index"),
        "client_login_url": url_for("client_login"),
        "organization_login_url": url_for("organization_login")
    }
    return render_template("select_role.html", **data)


# Клиент - вход
@app.route("/client/login")
def client_login() -> str:
    data: [str, object] = {
        "title": "Вход - клиент",
        "select_role_url": url_for("select_role"),
        "client_signup_url": url_for("client_signup")
    }
    return render_template("client_login.html", **data)


# Клиент - регистрация
@app.route("/client/signup")
def client_signup() -> str:
    data: [str, object] = {
        "title": "Регистрация - клиент",
        "select_role_url": url_for("select_role"),
        "client_login_url": url_for("client_login")
    }
    return render_template("client_signup.html", **data)


# Организация - вход
@app.route("/organization/login")
def organization_login() -> str:
    data: [str, object] = {
        "title": "Вход - организация",
        "select_role_url": url_for("select_role"),
        "organization_signup_url": url_for("organization_signup")
    }
    return render_template("organization_login.html", **data)


# Организация - регистрация
@app.route("/organization/signup")
def organization_signup() -> str:
    data: [str, object] = {
        "title": "Регистрация - организация",
        "select_role_url": url_for("select_role"),
        "organization_login_url": url_for("organization_login")
    }
    return render_template("organization_signup.html", **data)


# Отслеживание ошибок
@app.errorhandler(404)
def page_not_found_error(error_message):
    logger.info(error_message)
    return "404 Error", 404
