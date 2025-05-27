import uuid
import hmac
import hashlib
import requests

from typing import Optional
from haikiri.mikbill.response import Response
from haikiri.mikbill.request_abstract import RequestAbstract
from haikiri.mikbill.exceptions.BillApiException import BillApiException
from haikiri.mikbill.exceptions.UnauthorizedException import UnauthorizedException


class Request(RequestAbstract):

    def __init__(self, url: str, key: str, debug: bool = False):
        super().__init__(url, key, debug)

        # Работоспособность прокси, естественно никто не проверял.
        self.is_proxy = False
        self.proxy_type = "socks5"
        self.proxy_host = ""
        self.proxy_port = 8080
        self.proxy_user = ""
        self.proxy_pass = ""

    def send_request(
            self,
            uri: str,
            method: str = "POST",
            params: Optional[dict] = None,
            sign: bool = False,
            token: Optional[str] = None
    ):
        url = f"{self.url.rstrip('/')}/{uri.lstrip('/')}"
        headers = {}
        params = params or {}

        if sign:
            salt = uuid.uuid4().hex
            params["salt"] = salt
            params["sign"] = hmac.new(self.key.encode(), salt.encode(), hashlib.sha512).hexdigest()
        else:
            token = token or self.get_user_token()
            if not token: raise BillApiException("The token was not found: The storage with token is empty.")
            headers["Authorization"] = token

        proxies = None
        if self.is_proxy:
            auth = f"{self.proxy_user}:{self.proxy_pass}@" if self.proxy_user else ""
            scheme = url.split(":")[0]
            proxy_url = f"{self.proxy_type}://{auth}{self.proxy_host}:{self.proxy_port}"
            proxies = {scheme: proxy_url}

        # Отправку реального запроса, естественно никто не проверял.
        try:
            if method.upper() == "GET":
                res = requests.get(url, headers=headers, params=params, proxies=proxies)
            else:
                res = requests.post(url, headers=headers, data=params, proxies=proxies)

            res.raise_for_status()
        except Exception as ex:
            raise Exception(f"Request failed: {str(ex)}")

        if self.debug:
            print("**********")
            print(res.text)

        result = self.validate(res.text)
        self.bill_response_validate(result)
        return Response.from_response(result)

    @staticmethod
    def bill_response_validate(response: dict) -> None:
        if response.get("success", False) is True: return

        code = int(response.get("code", -1))
        message = response.get("message", "Unknown error")

        if code == -401:
            raise UnauthorizedException(message, code)
        else:
            raise BillApiException(message, code)
