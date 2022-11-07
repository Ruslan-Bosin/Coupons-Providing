from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField


# Формы входа/регистрации
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

# Форма нового купона
class NewRecordForm(FlaskForm):
    id = IntegerField("id")
    submit = SubmitField("checkout")

# Формы обновления данных профиля - клиент
class ClientChangeName(FlaskForm):
    name = StringField("name")
    submit = SubmitField("save")

# Формы обновления данных профиля - клиент
class ClientChangeEmail(FlaskForm):
    email = StringField("email")
    submit = SubmitField("save")
