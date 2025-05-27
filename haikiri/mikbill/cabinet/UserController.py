from haikiri.mikbill.request_abstract import RequestAbstract
from haikiri.mikbill.cabinet.user.User import User


class UserController:

    def __init__(self, interface: RequestAbstract):
        self.interface = interface

    def get_user(self) -> User:
        response = self.interface.send_request(
            uri="/api/v1/cabinet/user",
            method="GET",
            token=self.interface.get_user_token(),
        )
        return User(response)
