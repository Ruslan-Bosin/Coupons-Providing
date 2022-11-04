def email_validator(email: str) -> None | str:
    if "@" not in email:
        return "Некорректный адрес почты"
    return None


def password_validator(password: str) -> None | str:
    if len(password) < 8:
        return "Пароль слишком короткий"
    return None

# TODO: написать нормальные валидаторы
