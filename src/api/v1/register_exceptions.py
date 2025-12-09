from fastapi import FastAPI
from fastapi import HTTPException

from src.core.exceptions import (
    UserAlreadyExistsError,
    EntityNotFoundError,
    InvalidCredentialsError,
    PermissionDeniedError,
    DatabaseConnectionError,
    UniqueViolationError,
    TokenExpiredError,
    DuplicateEntryError,
    InvalidTokenError,
)

from src.api.v1.exception_handler import (
    user_already_exists_handler,
    entity_not_found_handler,
    invalid_credentials_handler,
    permission_denied_handler,
    unique_violation_handler,
    token_expired_handler,
    duplicate_entry_handler,
    invalid_token_handler,
    http_exception_handler,
    internal_server_error_handler,
    database_connection_error_handler,
)


def register_exception_handlers(app: FastAPI):

    # User-related
    app.add_exception_handler(UserAlreadyExistsError,
                              user_already_exists_handler)
    app.add_exception_handler(EntityNotFoundError, entity_not_found_handler)
    app.add_exception_handler(InvalidCredentialsError,
                              invalid_credentials_handler)
    app.add_exception_handler(PermissionDeniedError, permission_denied_handler)

    # Token-related
    app.add_exception_handler(TokenExpiredError, token_expired_handler)
    app.add_exception_handler(InvalidTokenError, invalid_token_handler)

    # Database
    app.add_exception_handler(DatabaseConnectionError,
                              database_connection_error_handler)
    app.add_exception_handler(UniqueViolationError, unique_violation_handler)
    app.add_exception_handler(DuplicateEntryError, duplicate_entry_handler)

    # HTTPException
    app.add_exception_handler(HTTPException, http_exception_handler)

    # Fallback
    app.add_exception_handler(Exception, internal_server_error_handler)
