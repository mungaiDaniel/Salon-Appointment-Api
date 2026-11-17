"""Uniform JSON error handling.

Every error response has the shape::

    {"status": 404, "code": "not_found", "message": "...", "details": {...}?}
"""

import logging

from flask import Flask, jsonify
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException

logger = logging.getLogger(__name__)


class ApiError(Exception):
    """An expected, client-facing error carrying an HTTP status and a stable error code."""

    def __init__(self, status: int, code: str, message: str, details: dict | None = None):
        super().__init__(message)
        self.status = status
        self.code = code
        self.message = message
        self.details = details


def bad_request(message="Bad request.", code="bad_request"):
    return ApiError(400, code, message)


def unauthorized(message="Authentication required.", code="unauthorized"):
    return ApiError(401, code, message)


def forbidden(message="You do not have permission to do that.", code="forbidden"):
    return ApiError(403, code, message)


def not_found(message="Resource not found.", code="not_found"):
    return ApiError(404, code, message)


def conflict(message="Resource already exists.", code="conflict"):
    return ApiError(409, code, message)


def error_response(status: int, code: str, message: str, details: dict | None = None):
    body = {"status": status, "code": code, "message": message}
    if details:
        body["details"] = details
    return jsonify(body), status


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(ApiError)
    def handle_api_error(err: ApiError):
        return error_response(err.status, err.code, err.message, err.details)

    @app.errorhandler(ValidationError)
    def handle_validation_error(err: ValidationError):
        return error_response(
            422, "validation_error", "Input validation failed.", err.normalized_messages()
        )

    @app.errorhandler(HTTPException)
    def handle_http_exception(err: HTTPException):
        code = (err.name or "error").lower().replace(" ", "_")
        return error_response(err.code or 500, code, err.description or err.name)

    @app.errorhandler(Exception)
    def handle_unexpected(err: Exception):
        logger.exception("Unhandled exception: %s", err)
        return error_response(500, "internal_error", "An unexpected error occurred.")
