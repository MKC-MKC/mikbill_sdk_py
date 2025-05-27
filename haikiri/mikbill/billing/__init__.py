from .UsersController import UsersController as Users


class Billing:

    def __init__(self, interface):
        self._interface = interface

    def users(self):
        return Users(self._interface)
