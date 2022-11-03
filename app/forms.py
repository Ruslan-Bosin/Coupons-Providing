from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField


class ClientLoginForm(FlaskForm):
    email = StringField("email")
    password = PasswordField("password")
    submit = SubmitField("login")
