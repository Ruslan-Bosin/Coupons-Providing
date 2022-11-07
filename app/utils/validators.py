def name_validator(name: str) -> None | str:
    if name == "aa":
        return "Введите настоящие имя"
    return None


def title_validator(title: str) -> None | str:
    if title == "aa":
        return "Введите настоящие название"
    return None


def email_validator(email: str) -> None | str:
    if "@" not in email:
        return "Некорректный адрес почты"
    return None


def password_validator(password: str) -> None | str:
    if len(password) < 8:
        return "Пароль слишком короткий"
    return None


def password_confirmation_validator(password: str, first_password: str) -> None | str:
    if password != first_password:
        return "Пароли не совпадают"
    return None

# TODO: написать нормальные валидаторы
