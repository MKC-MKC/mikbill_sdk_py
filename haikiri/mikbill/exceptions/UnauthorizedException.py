class UnauthorizedException(Exception):

    def __init__(self, message: str = "Ошибка авторизации", code: int = -401):
        super().__init__(message)
        self.code = code
