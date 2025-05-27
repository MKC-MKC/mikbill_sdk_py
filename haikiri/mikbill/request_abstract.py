import json

from typing import Optional
from abc import ABC, abstractmethod
from haikiri.mikbill.billing import Billing
from haikiri.mikbill.cabinet import Cabinet


class RequestAbstract(ABC):

    def __init__(self, url: str, key: str, debug: bool = False):
        self.url = url.rstrip("/")
        self.key = key
        self.debug = debug
        self.user_token: Optional[str] = None

        self.billing = Billing(self)
        self.cabinet = Cabinet(self)

    def set_user_token(self, token: str):
        self.user_token = token

    def get_user_token(self) -> str:
        return self.user_token or ""

    @staticmethod
    def validate(response_text: str):
        if not isinstance(response_text, str): raise ValueError("Invalid response from server: not a string")

        try:
            result = json.loads(response_text)
        except json.JSONDecodeError as exception:
            raise ValueError(f"Invalid JSON: {exception.msg}")

        return result

    @abstractmethod
    def send_request(self, uri: str, method: str, params: dict, sign: bool, token: Optional[str]):
        pass
