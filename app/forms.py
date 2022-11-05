from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField


class ClientLoginForm(FlaskForm):
    email = StringField("email")
    password = PasswordField("password")
    submit = SubmitField("login")


class ClientSignupForm(FlaskForm):
    name = StringField("name")
    email = StringField("email")
    password = PasswordField("password")
    password_confirmation = PasswordField("password_confirmation")
    submit = SubmitField("signup")


class OrganizationLoginForm(FlaskForm):
    email = StringField("email")
    password = PasswordField("password")
    submit = SubmitField("login")


class OrganizationSignupForm(FlaskForm):
    title = StringField("name")
    email = StringField("email")
    password = PasswordField("password")
    password_confirmation = PasswordField("password_confirmation")
    submit = SubmitField("signup")


class NewRecordForm(FlaskForm):
    id = IntegerField("id")
    submit = SubmitField("checkout")
