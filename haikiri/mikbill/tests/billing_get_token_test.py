from haikiri.mikbill.tests.mixin import InitMixin
from haikiri.mikbill.exceptions.UnauthorizedException import UnauthorizedException


class BillingGetTokenTest(InitMixin):
    debug = False
    sign_key = "mockedSignKey"
    token = "Bearer eyJ0eXAiOi.JKV1QiLCJ.hbGciOiJIUzI.1NiJ9"
    data_file = "responses/valid/Billing/Users/token.post.json"

    def test(self):
        try:
            # Получаем токен через billing
            token = self.MikBiLL.billing.users().get_user_token("здесь должен быть uid клиента")

            # Записываем токен в SDK
            self.MikBiLL.set_user_token(token)

            # Проверяем, что SDK хранит правильный токен
            current = self.MikBiLL.get_user_token()

            # Сверка результата.
            self.assertEqual(self.token, current)
        except UnauthorizedException as ex:
            print(str(ex))
            self.assertEqual(True, False, "ОШИБКА АВТОРИЗАЦИИ")
        except Exception as ex:
            print(str(ex))
            self.assertEqual(True, False, "Сработало исключение")
