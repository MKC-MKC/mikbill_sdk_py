from .UserController import UserController as User


class Cabinet:

    def __init__(self, interface):
        self._interface = interface

    def users(self):
        return User(self._interface)
