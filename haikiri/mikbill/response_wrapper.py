from typing import Optional, Any, Dict


class ResponseWrapper:

    def __init__(self, data: Optional[Dict[str, Any]]):
        self._data = data or {}

    def get_as_dict(self) -> Optional[Dict[str, Any]]:
        return self._data

    def get_data(self, key: Optional[str] = None, default: Any = None) -> Any:
        data = self._data
        if key is None: return data

        for part in key.split("."):
            if not isinstance(data, dict) or part not in data: return default
            data = data[part]

        return data
