from app import logger, login_manager
from app.models import ClientModel

# TODO: Обработку ошибок добавить


class User:

    _user = None
    _role = None

    def create_with_user_id(self, user_id: str):
        if user_id.startswith("c"):
            self._user = ClientModel.get(ClientModel.id == int(user_id[1::]))
            self._role = "client"
        elif user_id.startswith("o"):
            # TODO: self._user =
            self._role = "organization"
        else:
            logger.error(f"Неизвестный префикс user_id: {user_id}")
        return self

    def create_with_client_user(self, user):
        self._user = user
        self._role = "client"
        return self

    def create_with_organization_user(self, user):
        self._user = user
        self._role = "organization"
        return self

    def get_id(self):
        if self._role == "client":
            return f"c{self._user.id}"
        elif self._role == "organization":
            return f"o{self._user.id}"

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def is_active(self):
        return True

    def get_role(self):
        return "role/\\"


@login_manager.user_loader
def load_user(user_id: str):
    print(user_id)
    return User().create_with_user_id(user_id=user_id)
