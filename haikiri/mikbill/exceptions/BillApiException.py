class BillApiException(Exception):

    def __init__(self, message: str = "Unknown error", code: int = -1):
        super().__init__(message)
        self.code = code
