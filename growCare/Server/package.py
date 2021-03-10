from typing import Any


class Package:

    def __init__(self, device, response,requestCode, errorCode):
        self.device = device
        self.response = response
        self.requestCode = requestCode
        self.errorCode = errorCode

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)




