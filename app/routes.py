from app import app, logger
from flask import render_template, url_for, flash, redirect, abort
from app.forms import ClientLoginForm, ClientSignupForm, OrganizationLoginForm, OrganizationSignupForm
from app.utils.validators import name_validator, email_validator, password_validator, password_confirmation_validator, title_validator
from app.models import ClientModel, OrganizationModel
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.template_filters import style, script
from flask_login import login_user, login_required, current_user
from app.login import User


# Отслеживание URL
# Ознакомительная страница
@logger.catch
@app.route("/")
def index() -> str:

    data: [str, object] = {
        "title": "Главная страница",
        "start_url": url_for("select_role"),
        "ui_kit_styles_url": url_for("static", filename="css/ui_kit_styles.css"),
        "index_styles_url": url_for("static", filename="css/index_styles.css"),
        "index_script_url": url_for("static", filename="js/index_script.js"),
    }

    if isinstance(current_user, User):
        if current_user.is_client():
            data["start_url"] = url_for("client")
        elif current_user.is_organization():
            data["start_url"] = url_for("organization")

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
def client_login():
    form = ClientLoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        if email_validator(email) is None and password_validator(password) is None:
            client_account = ClientModel.get_or_none(ClientModel.email == email)
            if client_account and check_password_hash(client_account.password, password):
                user = User().create_with_client_user(user=client_account)
                login_user(user)
                return redirect(url_for("client"))
            else:
                flash("неверный логи и/или пароль")
        else:
            flash_message = str()
            if password_validator(password):
                flash_message = password_validator(password)
            if email_validator(email):
                flash_message = email_validator(email)
            flash(flash_message)

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
@app.route("/client/signup", methods=["POST", "GET"])
def client_signup():

    form = ClientSignupForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        password_confirmation = form.password_confirmation.data

        if name_validator(name) is None and email_validator(email) is None and password_validator(password) is None and password_confirmation_validator(password, password_confirmation) is None:
            email_taken = ClientModel.get_or_none(ClientModel.email == email)
            if email_taken:
                flash("Данный email уже занят")
            else:
                client_account = ClientModel(name=name, email=email, password=generate_password_hash(password))
                client_account.save()
                user = User().create_with_client_user(user=client_account)
                login_user(user)
                return redirect(url_for("client"))
        else:
            flash_message = str()
            if password_confirmation_validator(password, password_confirmation):
                flash_message = password_confirmation_validator(password, password_confirmation)
            if password_validator(password):
                flash_message = password_validator(password)
            if email_validator(email):
                flash_message = email_validator(email)
            if name_validator(name):
                flash_message = name_validator(name)
            flash(flash_message)

    data: [str, object] = {
        "title": "Регистрация - клиент",
        "select_role_url": url_for("select_role"),
        "client_login_url": url_for("client_login"),
        "ui_kit_styles_url": url_for("static", filename="css/ui_kit_styles.css"),
        "client_signup_styles_url": url_for("static", filename="css/client_signup_styles.css"),
        "client_signup_script_url": url_for("static", filename="js/client_signup_script.js"),
        "form": form,
    }
    return render_template("client_signup.html", **data)


# Основная страница - клиент
@logger.catch
@app.route("/client")
@login_required
def client() -> str:

    if current_user.is_organization():
        abort(401)

    data: [str, object] = {
        "title": "Клиент",
        "ui_kit_styles_url": url_for("static", filename="css/ui_kit_styles.css"),
        "client_styles_url": url_for("static", filename="css/client_styles.css"),
        "client_script_url": url_for("static", filename="js/client_script.js"),
        "user_id": current_user._user.to_dict()["id"],
        "data_js": {
            "user_id": current_user._user.to_dict()["id"]
        }
    }
    return render_template("client.html", **data)


# Организация - вход
@logger.catch
@app.route("/organization/login", methods=["POST", "GET"])
def organization_login():
    form = OrganizationLoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        if email_validator(email) is None and password_validator(password) is None:
            organization_account = OrganizationModel.get_or_none(OrganizationModel.email == email)
            if organization_account and check_password_hash(organization_account.password, password):
                user = User().create_with_organization_user(user=organization_account)
                login_user(user)
                return redirect(url_for("organization"))
            else:
                flash("неверный логи и/или пароль")
        else:
            flash_message = str()
            if password_validator(password):
                flash_message = password_validator(password)
            if email_validator(email):
                flash_message = email_validator(email)
            flash(flash_message)

    data: [str, object] = {
        "title": "Вход - организация",
        "select_role_url": url_for("select_role"),
        "organization_signup_url": url_for("organization_signup"),
        "ui_kit_styles_url": url_for("static", filename="css/ui_kit_styles.css"),
        "organization_login_styles_url": url_for("static", filename="css/organization_login_styles.css"),
        "organization_login_script_url": url_for("static", filename="js/organization_login_script.js"),
        "form": form,
    }
    return render_template("organization_login.html", **data)


# Организация - регистрация
@logger.catch
@app.route("/organization/signup", methods=["POST", "GET"])
def organization_signup():
    form = OrganizationSignupForm()

    if form.validate_on_submit():
        title = form.title.data
        email = form.email.data
        password = form.password.data
        password_confirmation = form.password_confirmation.data

        if name_validator(title) is None and email_validator(email) is None and password_validator(password) is None \
                and password_confirmation_validator(password, password_confirmation) is None:
            email_taken = OrganizationModel.get_or_none(OrganizationModel.email == email)
            if email_taken:
                flash("Данный email уже занят")
            else:
                organization_account = OrganizationModel(title=title, email=email, password=generate_password_hash(password))
                organization_account.save()
                user = User().create_with_organization_user(user=organization_account)
                login_user(user)
                return redirect(url_for("organization"))
        else:
            flash_message = str()
            if password_confirmation_validator(password, password_confirmation):
                flash_message = password_confirmation_validator(password, password_confirmation)
            if password_validator(password):
                flash_message = password_validator(password)
            if email_validator(email):
                flash_message = email_validator(email)
            if name_validator(title):
                flash_message = title_validator(email)
            flash(flash_message)

    data: [str, object] = {
        "title": "Регистрация - организация",
        "select_role_url": url_for("select_role"),
        "organization_login_url": url_for("organization_login"),
        "ui_kit_styles_url": url_for("static", filename="css/ui_kit_styles.css"),
        "organization_signup_styles_url": url_for("static", filename="css/organization_signup_styles.css"),
        "organization_signup_script_url": url_for("static", filename="js/organization_signup_script.js"),
        "form": form,
    }
    return render_template("organization_signup.html", **data)


# Основная страница - организация
@logger.catch
@app.route("/organization")
@login_required
def organization() -> str:

    if current_user.is_client():
        abort(401)

    data: [str, object] = {
        "title": "Организация",
        "ui_kit_styles_url": url_for("static", filename="css/ui_kit_styles.css"),
        "organization_styles_url": url_for("static", filename="css/organization_styles.css"),
        "organization_script_url": url_for("static", filename="js/organization_script.js"),
        "user_info": current_user._user.to_dict()
    }
    return render_template("organization.html", **data)

# Отслеживание ошибок
@logger.catch
@app.errorhandler(404)
def page_not_found_error(error_message):
    logger.info(error_message)
    return "404 Error", 404


@logger.catch
@app.errorhandler(401)
def page_not_found_error(error_message):
    logger.info(error_message)
    return "401 Error", 401
