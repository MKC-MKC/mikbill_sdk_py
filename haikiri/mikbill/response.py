from typing import Any, Optional


class Response:

    def __init__(
            self,
            success: bool,
            code: int,
            message: str,
            data: Optional[dict],
            raw: Any,
    ):
        self._success = success
        self._code = code
        self._message = message
        self._data = data
        self._raw = raw

    @classmethod
    def from_response(cls, response: dict) -> "Response":
        success = bool(response.get("success", False))
        code = int(response.get("code", response.get("error", -1)))
        message = str(response.get("message", response.get("errortext", "N/A")))

        data = response.get("data")
        if not isinstance(data, dict):
            data = None

        return cls(
            success=success,
            code=code,
            message=message,
            data=data,
            raw=response,
        )

    def is_success(self) -> bool:
        return self._success

    def get_code(self) -> int:
        return self._code

    def get_message(self) -> str:
        return self._message

    def get_raw(self) -> Any:
        return self._raw

    def get_data(self) -> Optional[dict]:
        return self._data

    def get_token(self) -> Optional[str]:
        if not self._data: return None
        return self._data.get("token")
