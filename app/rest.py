from config import SECRET_KEY
from app import app, logger
from app.models import ClientModel, OrganizationModel, RecordModel, AdminModel
from app.utils.token_required import token_required
from app.utils.validators import *
from flask import request, jsonify, make_response, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta, date


# Клиент
@app.route("/rest/client/login", methods=["POST"])
def rest_client_login():

    data: dict = request.get_json()
    email: str = data.get("email")
    password: str = data.get("password")

    if not email or not password:
        return make_response(jsonify({"message": "could not verify"}), 401)

    client = ClientModel.get_or_none(ClientModel.email == email)
    if not client:
        return make_response(jsonify({"message": "could not verify"}), 401)
    if not check_password_hash(client.password, password):
        return make_response(jsonify({"message": "could not verify"}), 401)

    token = jwt.encode({"role": "client", "id": client.id, "exp": datetime.utcnow() + timedelta(days=30)}, SECRET_KEY)

    return jsonify({"message": "successfully logged in", "token": token})


@app.route("/rest/client/signup", methods=["POST"])
def rest_client_signup():

    data: dict = request.get_json()
    name: str = data.get("name")
    email: str = data.get("email")
    password: str = data.get("password")

    if not name or not email or not password:
        return make_response(jsonify({"message": "parameters missing"}), 400)

    email_taken = ClientModel.get_or_none(ClientModel.email == email)
    if email_taken:
        return make_response(jsonify({"message": "email taken"}), 417)

    if name_validator(name) is None and email_validator(email) is None and password_validator(password) is None:
        client_account = ClientModel(name=name, email=email, password=generate_password_hash(password))
        client_account.save()
    else:
        message = str()
        if password_validator(password):
            message = password_validator(password)
        if email_validator(email):
            message = email_validator(email)
        if name_validator(name):
            message = name_validator(name)
        return make_response(jsonify({"message": message}), 417)

    return jsonify({"message": "account created"})


@app.route("/rest/client/active", methods=["GET"])
@token_required
def rest_client_active(rest_user):

    if not isinstance(rest_user, ClientModel):
        return make_response(jsonify({"message": "only the client has access"}), 401)

    data = RecordModel.select().where(RecordModel.client == rest_user.id).order_by(RecordModel.accumulated.desc())
    result = [{"image": url_for('organization_picture_get', id=item.organization.id),
               "title": item.organization.title,
               "accumulated": item.accumulated,
               "limit": item.organization.limit} for item in data]

    return jsonify(result)


@app.route("/rest/client/info", methods=["GET"])
@token_required
def rest_client_info(rest_user):

    if not isinstance(rest_user, ClientModel):
        return make_response(jsonify({"message": "only the client has access"}), 401)

    result = {
        "id": rest_user.id,
        "name": rest_user.name,
        "email": rest_user.email,
        "is_private": rest_user.is_private
    }

    return jsonify(result)


@app.route("/rest/client/info", methods=["PUT"])
@token_required
def rest_client_change(rest_user):

    if not isinstance(rest_user, ClientModel):
        return make_response(jsonify({"message": "only the client has access"}), 401)

    data: dict = request.get_json()
    name: str = data.get("name")
    email: str = data.get("email")
    password: str = data.get("password")
    is_private: bool = data.get("is_private")

    changed = list()
    if name is not None:
        if name_validator(name) is None:
            client = ClientModel.get_or_none(ClientModel.id == rest_user.id)
            client.name = name
            client.save()
            changed.append("name")
        else:
            return make_response(jsonify({"message": f"name is not valid - {name_validator(name)}"}), 417)
    if email is not None:
        if email_validator(email) is None:
            client = ClientModel.get_or_none(ClientModel.id == rest_user.id)
            client.email = email
            client.save()
            changed.append("email")
        else:
            return make_response(jsonify({"message": f"email is not valid - {email_validator(email)}"}), 417)
    if password is not None:
        if password_validator(password) is None:
            client = ClientModel.get_or_none(ClientModel.id == rest_user.id)
            client.password = generate_password_hash(password)
            client.save()
            changed.append("password")
        else:
            return make_response(jsonify({"message": f"password is not valid - {password_validator(password)}"}), 417)
    if is_private is not None:
        client = ClientModel.get_or_none(ClientModel.id == rest_user.id)
        client.is_private = is_private
        client.save()
        changed.append("is_private")

    if changed:
        return jsonify({"message": f"{', '.join(changed)} updated"})

    return make_response(jsonify({"message": "nothing updated"}), 417)


# Организация
@app.route("/rest/organization/login", methods=["POST"])
def rest_organization_login():

    data: dict = request.get_json()
    email: str = data.get("email")
    password: str = data.get("password")

    if not email or not password:
        return make_response(jsonify({"message": "could not verify"}), 401)

    organization = OrganizationModel.get_or_none(OrganizationModel.email == email)
    if not organization:
        return make_response(jsonify({"message": "could not verify"}), 401)
    if not check_password_hash(organization.password, password):
        return make_response(jsonify({"message": "could not verify"}), 401)

    token = jwt.encode({"role": "organization", "id": organization.id, "exp": datetime.utcnow() + timedelta(days=30)}, SECRET_KEY)

    return jsonify({"message": "successfully logged in", "token": token})


@app.route("/rest/organization/signup", methods=["POST"])
def rest_organization_signup():

    data: dict = request.get_json()
    title: str = data.get("title")
    email: str = data.get("email")
    password: str = data.get("password")

    if not title or not email or not password:
        return make_response(jsonify({"message": "parameters missing"}), 400)

    email_taken = OrganizationModel.get_or_none(OrganizationModel.email == email)
    if email_taken:
        return make_response(jsonify({"message": "email taken"}), 417)

    if title_validator(title) is None and email_validator(email) is None and password_validator(password) is None:
        organization_account = OrganizationModel(title=title, email=email, password=generate_password_hash(password))
        organization_account.save()
    else:
        message = str()
        if password_validator(password):
            message = password_validator(password)
        if email_validator(email):
            message = email_validator(email)
        if title_validator(title):
            message = title_validator(title)
        return make_response(jsonify({"message": message}), 417)

    return jsonify({"message": "account created"})


@app.route("/rest/organization/clients", methods=["GET"])
@token_required
def rest_organization_active(rest_user):

    if not isinstance(rest_user, OrganizationModel):
        return make_response(jsonify({"message": "only the organization has access"}), 401)

    data = RecordModel.select().where(RecordModel.organization == rest_user.id).order_by(RecordModel.accumulated.desc())
    result = [{"name": item.client.name,
               "is_private": item.client.is_private,
               "accumulated": item.accumulated,
               "limit": item.organization.limit} for item in data]

    return jsonify(result)


@app.route("/rest/organization/info", methods=["GET"])
@token_required
def rest_organization_info(rest_user):

    if not isinstance(rest_user, OrganizationModel):
        return make_response(jsonify({"message": "only the organization has access"}), 401)

    result = {
        "id": rest_user.id,
        "title": rest_user.title,
        "email": rest_user.email,
        "sticker": rest_user.sticker,
        "limit": rest_user.limit,
        "image": url_for('organization_picture_get', id=rest_user.id) if rest_user.image else None,
    }

    return jsonify(result)


@app.route("/rest/organization/info", methods=["PUT"])
@token_required
def rest_organization_change(rest_user):

    if not isinstance(rest_user, OrganizationModel):
        return make_response(jsonify({"message": "only the organization has access"}), 401)

    data: dict = request.get_json()
    title: str = data.get("title")
    email: str = data.get("email")
    password: str = data.get("password")
    sticker: str = data.get("sticker")
    limit: int = data.get("limit")

    changed = list()
    if title is not None:
        if title_validator(title) is None:
            organization = OrganizationModel.get_or_none(OrganizationModel.id == rest_user.id)
            organization.title = title
            organization.save()
            changed.append("title")
        else:
            return make_response(jsonify({"message": f"title is not valid - {title_validator(title)}"}), 417)
    if email is not None:
        if email_validator(email) is None:
            organization = OrganizationModel.get_or_none(OrganizationModel.id == rest_user.id)
            organization.email = email
            organization.save()
            changed.append("email")
        else:
            return make_response(jsonify({"message": f"email is not valid - {email_validator(email)}"}), 417)
    if password is not None:
        if password_validator(password) is None:
            organization = OrganizationModel.get_or_none(OrganizationModel.id == rest_user.id)
            organization.password = generate_password_hash(password)
            organization.save()
            changed.append("password")
        else:
            return make_response(jsonify({"message": f"password is not valid - {password_validator(password)}"}), 417)
    if sticker is not None:
        if sticker_validator(sticker) is None:
            organization = OrganizationModel.get_or_none(OrganizationModel.id == rest_user.id)
            organization.sticker = sticker
            organization.save()
            changed.append("sticker")
        else:
            return make_response(jsonify({"message": f"sticker is not valid - {sticker_validator(sticker)}"}), 417)
    if limit is not None:
        if limit_validator(limit) is None:
            organization = OrganizationModel.get_or_none(OrganizationModel.id == rest_user.id)
            organization.limit = limit
            organization.save()
            changed.append("limit")
        else:
            return make_response(jsonify({"message": f"limit is not valid - {limit_validator(limit)}"}), 417)

    if changed:
        return jsonify({"message": f"{', '.join(changed)} updated"})

    return make_response(jsonify({"message": "nothing updated"}), 417)


@app.route("/rest/organization/upload", methods=["POST"])
@token_required
def rest_organization_change_picture_upload(rest_user):

    if not isinstance(rest_user, OrganizationModel):
        return make_response(jsonify({"message": "only the organization has access"}), 401)

    if "file" not in request.files:
        return make_response(jsonify({"message": "No file part in the request"}), 400)

    file = request.files['file']
    if file.filename == "":
        return make_response(jsonify({"message": "No file selected for uploading"}), 400)

    if file and image_validator(file.filename) is None:
        image = file.read()
        from sqlite3 import Binary  # TODO: change (remove sqlite3)
        bin_image = Binary(image)

        organization = OrganizationModel.get(OrganizationModel.id == rest_user.id)
        organization.image = bin_image
        organization.save()
        return jsonify({"message": "File successfully uploaded"})
    else:
        return make_response(jsonify({"message": f"{image_validator(file.filename)}"}), 400)


@app.route("/rest/organization/record", methods=["PUT"])
@token_required
def rest_organization_record(rest_user):

    if not isinstance(rest_user, OrganizationModel):
        return make_response(jsonify({"message": "only the organization has access"}), 401)

    data: dict = request.get_json()
    id: int = data.get("id")

    if not id:
        return make_response(jsonify({"message": "missing id"}), 400)

    client_exists = ClientModel.get_or_none(ClientModel.id == id)

    if client_exists:
        record_exists = RecordModel.get_or_none((RecordModel.client == id) & (RecordModel.organization == rest_user.id))

        if record_exists:
            record_exists.accumulated += 1
            record_exists.last_record_date = date.today()

            if record_exists.accumulated >= rest_user.limit:
                record_exists.accumulated = 0
                record_exists.save()
                return jsonify({"message": "accumulated"})

            record_exists.save()
            return jsonify({"message": "added"})
        else:
            RecordModel(client=id, organization=rest_user.id, last_record_date=date.today()).save()
            return jsonify({"message": "record added"})
    else:
        return make_response(jsonify({"message": "wrong id"}), 417)


# Администрация
@app.route("/rest/admin/login", methods=["POST"])
def rest_admin_login():

    data: dict = request.get_json()
    email: str = data.get("email")
    password: str = data.get("password")

    if not email or not password:
        return make_response(jsonify({"message": "could not verify"}), 401)

    admin = AdminModel.get_or_none(AdminModel.email == email)
    if not admin:
        return make_response(jsonify({"message": "could not verify"}), 401)
    if not check_password_hash(admin.password, password):
        return make_response(jsonify({"message": "could not verify"}), 401)

    token = jwt.encode({"role": "admin", "id": admin.id, "exp": datetime.utcnow() + timedelta(hours=12)}, SECRET_KEY)

    return jsonify({"message": "successfully logged in", "token": token})


@app.route("/rest/admin/clients", methods=["GET"])
@token_required
def rest_admin_clients(rest_user):

    if not isinstance(rest_user, AdminModel):
        return make_response(jsonify({"message": "no admin access"}), 401)

    data = ClientModel.select()
    result = list()
    for item in data:
        result.append({
            "id": item.id,
            "name": item.name,
            "email": item.email,
            "password": item.password,
            "is_private": item.is_private
        })

    return jsonify(result)


# Адрес для выяснения включен ли сервер
@app.route("/rest/is_server_on", methods=["GET"])
def rest_is_server_on():
    return jsonify({"message": "server is on"})


# Проверка админ token-а
@app.route("/rest/admin/verify_token", methods=["GET"])
@token_required
def rest_admin_verify_token(rest_user):

    if not isinstance(rest_user, AdminModel):
        return make_response(jsonify({"message": "no admin access"}), 401)

    return jsonify({"message": "token is valid"})
