import json
import unittest

from haikiri.mikbill.tests.mock import MikBiLLApiMock


class InitMixin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Поясняем за переменные.
        super().setUpClass()
        data_file = getattr(cls, "data_file", None)
        sign_key = getattr(cls, "sign_key", "")
        debug = getattr(cls, "debug", False)
        token = getattr(cls, "token", "")

        # Не можем работать без данных.
        if not data_file: raise ValueError("Missing data_file in test class.")

        # Открываем файл.
        with open(data_file, "r", encoding="utf-8") as payload:
            mocked_data = json.load(payload)

        # Инициализация MikBiLL SDK.
        cls.MikBiLL = MikBiLLApiMock(
            url="http://api.mikbill.local",
            key=sign_key,
            debug=debug,
            mocked_data=mocked_data,
        )

        # Записываем токен пользователя.
        cls.MikBiLL.set_user_token(token)
