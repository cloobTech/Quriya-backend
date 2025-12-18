from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class QuriyaError(Exception):
    """Base class for all Quriya exceptions."""
    message: str
    details: Optional[Any] = None

    # def __str__(self):
    #     return self.message


class UserAlreadyExistsError(QuriyaError):
    def __init__(self, message="User already exists", details=None):
        super().__init__(message=message, details=details)


class EntityNotFoundError(QuriyaError):
    """Raised when an entity (user, organization, etc.) is not found."""

    def __init__(self, message="Entity not found", details=None):
        super().__init__(message=message, details=details)


class InvalidCredentialsError(QuriyaError):
    """Raised when login credentials are invalid."""

    def __init__(self, message="Invalid username or password", details=None):
        super().__init__(message=message, details=details)


class PermissionDeniedError(QuriyaError):
    """Raised when a user tries to access something they don't have permission for."""

    def __init__(self, message="You do not have permission to perform this action", details=None):
        super().__init__(message=message, details=details)


class DatabaseConnectionError(QuriyaError):
    """Raised when the system cannot connect to the database."""

    def __init__(self, message="Failed to connect to the database", details=None):
        super().__init__(message=message, details=details)


class TokenExpiredError(QuriyaError):
    """Raised when an authentication token has expired."""

    def __init__(self, message="Token has expired", details=None):
        super().__init__(message=message, details=details)


class InvalidTokenError(QuriyaError):
    """Raised when an authentication token is invalid."""

    def __init__(self, message="Invalid authentication token", details=None):
        super().__init__(message=message, details=details)


class DuplicateEntryError(QuriyaError):
    """Raised when attempting to insert a duplicate record."""

    def __init__(self, message="Duplicate entry detected", details=None):
        super().__init__(message=message, details=details)


class UniqueViolationError(QuriyaError):
    """Raised when a database unique constraint is violated."""

    def __init__(self, message="A unique constraint was violated", details=None):
        super().__init__(message=message, details=details)


class InvalidCoverageSelectionError(QuriyaError):
    """Raised when a no location coverage is passed from the frontend"""

    def __init__(self, message="At least one coverage level must be selected", details=None):
        super().__init__(message=message, details=details)
