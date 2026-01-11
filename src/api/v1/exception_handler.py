from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from src.schemas.error import ErrorResponse


def user_already_exists_handler(request: Request, exc: Exception):

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=ErrorResponse(
            error="user_already_exists",
            message=getattr(exc, "message", ""),
            details=getattr(exc, "details", None)
        ).model_dump(),
    )


def entity_not_found_handler(request: Request, exc: Exception):

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=ErrorResponse(
            error="entity_not_found",
            message=getattr(exc, "message", ""),
            details=getattr(exc, "details", None),

        ).model_dump(),
    )


def invalid_credentials_handler(request: Request, exc: Exception):

    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=ErrorResponse(
            error="invalid_credentials",
            message=getattr(exc, "message", ""),
            details=getattr(exc, "details", None),

        ).model_dump(),
    )


def permission_denied_handler(request: Request, exc: Exception):

    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content=ErrorResponse(
            error="permission_denied",
            message=getattr(exc, "message", ""),
            details=getattr(exc, "details", None),

        ).model_dump(),
    )


def unique_violation_handler(request: Request, exc: Exception):

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=ErrorResponse(
            error="unique_violation",
            message=getattr(exc, "message", ""),
            details=getattr(exc, "details", None),

        ).model_dump(),
    )


def invalid_coverage_selection(request: Request, exc: Exception):

    return JSONResponse(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        content=ErrorResponse(
            error="invalid_coverage",
            message=getattr(exc, "message", ""),
            details=getattr(exc, "details", None),

        ).model_dump(),
    )


def token_expired_handler(request: Request, exc: Exception):

    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=ErrorResponse(
            error="token_expired",
            message=getattr(exc, "message", ""),
            details=getattr(exc, "details", None),

        ).model_dump(),
    )


def invalid_token_handler(request: Request, exc: Exception):

    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=ErrorResponse(
            error="invalid_token",
            message=getattr(exc, "message", ""),
            details=getattr(exc, "details", None),

        ).model_dump(),
    )


def duplicate_entry_handler(request: Request, exc: Exception):

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=ErrorResponse(
            error="duplicate_entry",
            message=getattr(exc, "message", ""),
            details=getattr(exc, "details", None),

        ).model_dump(),
    )


def database_connection_error_handler(request: Request, exc: Exception):

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="database_connection_error",
            message=getattr(exc, "message", ""),
            details=getattr(exc, "details", None),

        ).model_dump(),
    )


def http_exception_handler(request: Request, exc: Exception):

    return JSONResponse(
        status_code=exc.status_code if isinstance(
            exc, HTTPException) else status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="http_exception",
            message=exc.detail if isinstance(
                exc, HTTPException) else "An unexpected error occurred.",
        ).model_dump(),
    )


def internal_server_error_handler(request: Request, exc: Exception):

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="internal_server_error",
            message="An unexpected error occurred.",
            details={"original_error": str(exc)},
        ).model_dump(),
    )
