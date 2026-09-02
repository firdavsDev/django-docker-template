import logging

from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

logger = logging.getLogger("src")


class CustomException(APIException):
    """Base for project domain errors. Subclass with concrete defaults:

        class InsufficientBalance(CustomException):
            status_code = 402
            default_detail = "Insufficient balance."
            default_code = "insufficient_balance"

    Raised anywhere, it flows through ``custom_exception_handler`` into the
    ``{"status": "error", "message": ...}`` envelope.
    """

    status_code = 400
    default_detail = "A server error occurred."
    default_code = "error"


def _flatten_detail(detail) -> str:
    """Reduce a DRF error detail (str | list | dict, nested) to one message."""
    if isinstance(detail, dict):
        for value in detail.values():
            message = _flatten_detail(value)
            if message:
                return message
        return ""
    if isinstance(detail, list | tuple):
        for item in detail:
            message = _flatten_detail(item)
            if message:
                return message
        return ""
    return str(detail)


def custom_exception_handler(exc, context):
    """Reshape every DRF exception into the CustomResponseMixin envelope:

        {"status": "error", "message": "..."}

    Non-DRF exceptions: re-raised under DEBUG so the traceback page shows;
    otherwise logged (Sentry picks up the ERROR log) and returned as the same
    JSON envelope with a 500 so API clients never get an HTML error page.
    """
    response = drf_exception_handler(exc, context)
    if response is None:
        if settings.DEBUG:
            return None
        request = context.get("request")
        logger.exception("Unhandled exception at %s", getattr(request, "path", "?"))
        return Response(
            {"status": "error", "message": "Internal server error."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    detail = response.data
    payload = {
        "status": "error",
        "message": _flatten_detail(detail),
    }
    # Expose per-field errors only when DRF gives a field->messages mapping.
    if isinstance(detail, dict):
        payload["errors"] = detail

    response.data = payload
    return response
