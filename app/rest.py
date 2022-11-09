from config import SECRET_KEY
from app import app, logger
from app.models import ClientModel, OrganizationModel, RecordModel
from app.utils.token_required import token_required
from app.utils.validators import *
from flask import request, jsonify, make_response, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta


@app.route("/rest/client/login", methods=["POST"])
def rest_organization_login():

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
def rest_organization_signup():

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
def rest_organization_active(rest_user):

    if not isinstance(rest_user, ClientModel):
        return jsonify({"message": "only the client has access"})

    data = RecordModel.select().where(RecordModel.client == rest_user.id).order_by(RecordModel.accumulated.desc())
    result = [{"image": url_for('organization_picture_get', id=item.organization.id),
               "title": item.organization.title,
               "accumulated": item.accumulated,
               "limit": item.organization.limit} for item in data]

    return jsonify(result)


@app.route("/rest/client/info", methods=["GET"])
@token_required
def rest_organization_info(rest_user):

    if not isinstance(rest_user, ClientModel):
        return jsonify({"message": "only the client has access"})

    result = {
        "id": rest_user.id,
        "name": rest_user.name,
        "email": rest_user.email,
        "is_private": rest_user.is_private
    }

    return jsonify(result)


@app.route("/rest/client/info", methods=["PUT"])
@token_required
def rest_organization_change(rest_user):

    if not isinstance(rest_user, ClientModel):
        return jsonify({"message": "only the client has access"})

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

