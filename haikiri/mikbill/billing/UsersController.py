from haikiri.mikbill.billing.users.Search import Search


class UsersController:

    def __init__(self, billing_interface):
        self.interface = billing_interface

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
            method="POST",
            params=params,
            sign=True,
        )

        return response.get_token()
