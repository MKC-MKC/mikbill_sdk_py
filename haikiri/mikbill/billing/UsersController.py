from haikiri.mikbill.request_abstract import RequestAbstract
from haikiri.mikbill.billing.users.Search import Search


class UsersController:

    def __init__(self, interface: RequestAbstract):
        self.interface = interface

    def search_user(self, key="uid", value="1", operator="="):
        params = {
            "field": key,
            "operator": operator,
            "value": value
        }

        response = self.interface.send_request(
            uri="/api/v1/billing/users/search",
            method="GET",
            params=params,
            sign=True,
        )

        return Search(response)

    def get_user_token(self, uid: int) -> str:
        params = {"uid": uid}

        response = self.interface.send_request(
            uri="/api/v1/billing/users/token",
            params=params,
            sign=True,
        )

        return response.get_token()
