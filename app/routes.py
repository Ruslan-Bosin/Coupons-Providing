from app import app, logger
from flask import render_template, url_for
from app.forms import ClientLoginForm
from app.utils import style


# Отслеживание URL
# Ознакомительная страница
@logger.catch
@app.route("/")
def index() -> str:
    data: [str, object] = {
        "title": "Главная страница",
        "select_role_url": url_for("select_role"),
        "ui_kit_styles_url": url_for("static", filename="css/ui_kit_styles.css"),
        "index_styles_url": url_for("static", filename="css/index_styles.css"),
        "index_script_url": url_for("static", filename="js/index_script.js"),
    }
    return render_template("index.html", **data)


# Выбор роли: клиент / организация
@logger.catch
@app.route("/select_role")
def select_role() -> str:
    data_html: [str, object] = {
        "title": "Выберите кто вы",
        "index_url": url_for("index"),
        "client_login_url": url_for("client_login"),
        "organization_login_url": url_for("organization_login"),
        "ui_kit_styles_url": url_for("static", filename="css/ui_kit_styles.css"),
        "select_role_styles_url": url_for("static", filename="css/select_role_styles.css"),
        "select_role_script_url": url_for("static", filename="js/select_role_script.js"),
    }
    return render_template("select_role.html", **data_html)


# Клиент - вход
@logger.catch
@app.route("/client/login", methods=["POST", "GET"])
def client_login() -> str:
    form = ClientLoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data


    data: [str, object] = {
        "title": "Вход - клиент",
        "select_role_url": url_for("select_role"),
        "client_signup_url": url_for("client_signup"),
        "ui_kit_styles_url": url_for("static", filename="css/ui_kit_styles.css"),
        "client_login_styles_url": url_for("static", filename="css/client_login_styles.css"),
        "client_login_script_url": url_for("static", filename="js/client_login_script.js"),
        "form": form,
    }
    return render_template("client_login.html", **data)


# Клиент - регистрация
@logger.catch
@app.route("/client/signup")
def client_signup() -> str:
    data: [str, object] = {
        "title": "Регистрация - клиент",
        "select_role_url": url_for("select_role"),
        "client_login_url": url_for("client_login"),
        "ui_kit_styles_url": url_for("static", filename="css/ui_kit_styles.css"),
        "client_signup_styles_url": url_for("static", filename="css/client_signup_styles.css"),
        "client_signup_script_url": url_for("static", filename="js/client_signup_script.js"),
    }
    return render_template("client_signup.html", **data)


# Основная страница - клиент
@logger.catch
@app.route("/client")
def client() -> str:
    data: [str, object] = {
        "title": "Клиент",
        "ui_kit_styles_url": url_for("static", filename="css/ui_kit_styles.css"),
        "client_styles_url": url_for("static", filename="css/client_styles.css"),
        "client_script_url": url_for("static", filename="js/client_script.js"),
    }
    return render_template("client.html", **data)


# Организация - вход
@logger.catch
@app.route("/organization/login")
def organization_login() -> str:
    data: [str, object] = {
        "title": "Вход - организация",
        "select_role_url": url_for("select_role"),
        "organization_signup_url": url_for("organization_signup"),
        "ui_kit_styles_url": url_for("static", filename="css/ui_kit_styles.css"),
        "organization_login_styles_url": url_for("static", filename="css/organization_login_styles.css"),
        "organization_login_script_url": url_for("static", filename="js/organization_login_script.js"),
    }
    return render_template("organization_login.html", **data)


# Организация - регистрация
@logger.catch
@app.route("/organization/signup")
def organization_signup() -> str:
    data: [str, object] = {
        "title": "Регистрация - организация",
        "select_role_url": url_for("select_role"),
        "organization_login_url": url_for("organization_login"),
        "ui_kit_styles_url": url_for("static", filename="css/ui_kit_styles.css"),
        "organization_signup_styles_url": url_for("static", filename="css/organization_signup_styles.css"),
        "organization_signup_script_url": url_for("static", filename="js/organization_signup_script.js"),
    }
    return render_template("organization_signup.html", **data)


# Отслеживание ошибок
@logger.catch
@app.errorhandler(404)
def page_not_found_error(error_message):
    logger.info(error_message)
    return "404 Error", 404
