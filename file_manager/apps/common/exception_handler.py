from typing import Any, Dict, Type

from apps.common.exceptions import CustomApiException
from django.core.exceptions import PermissionDenied
from django.http.response import Http404
from rest_framework import exceptions, views
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


def api_exception_handler(exc: Type[Exception], context: Dict[str, Any]) -> Response | None:
    """
    Mostly copied from rest-framework
    Returns the response that should be used for any given exception.
    Can append 'extra' field on returned data.

    By default, we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """

    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, "auth_header", None):
            headers["WWW-Authenticate"] = exc.auth_header  # noqa
        if getattr(exc, "wait", None):
            headers["Retry-After"] = "%d" % exc.wait  # noqa

        if isinstance(exc.detail, dict):
            data = {"details_json": exc.detail}  # Request from the front-end to rename the field if returning a dict
        elif isinstance(exc.detail, list):
            data = {"details": exc.detail}
        else:  # Exc detail is string.
            data = {"detail": exc.detail}

        if isinstance(exc, ValidationError):
            data["error_code"] = 999999  # noqa
        elif isinstance(exc, CustomApiException):
            extra = exc.get_extra()
            if extra:
                data["extra"] = extra
            error_code = exc.get_error_code()
            if error_code:
                parse_error_code_to_int = True
                if parse_error_code_to_int:
                    data["error_code"] = int(error_code)  # noqa
                else:
                    data["error_code"] = error_code  # noqa

        views.set_rollback()
        return Response(data, status=exc.status_code, headers=headers)
    return None
