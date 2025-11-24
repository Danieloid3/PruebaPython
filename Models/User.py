# Models/User.py
class User:
    __idActual = 1

    def __init__(self, name: str, username: str, password: str, role: int, user_id: int | None = None):
        if user_id is None:
            self._userID = User.__idActual
            User.__idActual += 1
        else:
            self._userID = int(user_id)
            if self._userID >= User.__idActual:
                User.__idActual = self._userID + 1
        self._name = name
        self._username = username
        self._password = password
        self._role = role

    @property
    def userID(self) -> int:
        return self._userID

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, value: str):
        self._username = value

    @property
    def password(self) -> str:

        return self._password

    @password.setter
    def password(self, value: str):
        self._password = value

    @property
    def role(self) -> int:
        return self._role

    @role.setter
    def role(self, value: int):
        self._role = value
