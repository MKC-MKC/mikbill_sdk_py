from typing import Optional
from haikiri.mikbill.response_wrapper import ResponseWrapper


class User(ResponseWrapper):

    def get_username(self) -> Optional[str]:
        return self.get_data("username")

    def get_user_tariff_name(self) -> Optional[str]:
        return self.get_data("packet_name")
