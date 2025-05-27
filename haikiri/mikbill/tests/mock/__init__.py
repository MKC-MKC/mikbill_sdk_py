import hashlib
import hmac
import uuid

from haikiri.mikbill.request import Request
from haikiri.mikbill.response import Response
from haikiri.mikbill.exceptions.UnauthorizedException import UnauthorizedException


class MikBiLLApiMock(Request):
    _mocked_data = None
    _received_key = None
    _expected_key = "mockedSignKey"
    _expected_token = "Bearer eyJ0eXAiOi.JKV1QiLCJ.hbGciOiJIUzI.1NiJ9"

    def __init__(self, url: str, key: str, debug: bool = False, mocked_data=None):
        super().__init__(url, key, debug)
        MikBiLLApiMock._received_key = key
        MikBiLLApiMock._mocked_data = mocked_data

    def send_request(self, uri: str, method: str = "POST", params: dict = None, sign: bool = False, token: str = None):
        # По умолчанию готовим переданный ответ.
        response = MikBiLLApiMock._mocked_data

        # Подпись запроса.
        if sign:
            # Генерация ключа HMAC.
            salt = uuid.uuid4().hex
            local_sign = hmac.new(MikBiLLApiMock._received_key.encode(), salt.encode(), hashlib.sha512).hexdigest()
            expected_sign = hmac.new(MikBiLLApiMock._expected_key.encode(), salt.encode(), hashlib.sha512).hexdigest()

            # Если включена "отладка".
            if self.debug:
                print("SALT:", salt)
                print("SIGN:", local_sign)

            # Имитируем проверку ключа на стороне Api.
            if not hmac.compare_digest(expected_sign, local_sign): response = self.on_unauthorized()
        else:
            if self.debug:
                print("Received Token:", token)
                print("Expected Token:", MikBiLLApiMock._expected_token)

            # Если передали пустой токен, значит произошла ошибка при его формировании.
            if token == "":
                raise UnauthorizedException("The token was not found: The storage with token is empty.")
            elif token != MikBiLLApiMock._expected_token:
                response = self.on_unauthorized()

        # Проверяем и возвращаем данные.
        if isinstance(response, str):
            valid = self.validate(response)
        else:
            valid = response

        # Проверяем наш ответ на ошибки MikBiLL.
        self.bill_response_validate(valid)

        # Возвращаем объект ответа.
        return Response.from_response(valid)

    @staticmethod
    def on_unauthorized() -> str:
        path = "responses/invalid/401-unauthorized.json"
        with open(path, "r", encoding="utf-8") as f: return f.read()
