from domain.errors import BaseError


class C3GateWayError(BaseError):
    @property
    def message(self) -> str:
        return "C3 error"
