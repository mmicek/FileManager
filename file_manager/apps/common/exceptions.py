from typing import Type

from rest_framework import exceptions, status


class CustomApiException(exceptions.APIException):
    """
    Custom API Exception class extending DRF's APIException.
    """

    status_code: int = status.HTTP_400_BAD_REQUEST
    default_detail: str = "Request cannot be processed."
    error_code: int | None = None
    wrapped_exception: Type["CustomApiException"] | None = None

    def __init__(self, *args, extra: dict | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        assert self.error_code
        self.args = (self.detail,)
        self.extra = extra

    def get_extra(self) -> dict | None:
        return self.extra

    def get_error_code(self) -> int:
        assert self.error_code
        return self.error_code

    @classmethod
    def wrap(cls, exception: Type["CustomApiException"]) -> "CustomApiException":
        wrapper = cls(*exception.args)
        wrapper.wrapped_exception = exception
        return wrapper
