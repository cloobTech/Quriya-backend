import bcrypt
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from src.core.pydantic_config import config
from src.models.user import User
from src.core.exceptions import InvalidCredentialsError


def hash_password(password: str) -> str:
    """ hash password """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(user: User, password: str) -> bool:
    """Verify Password"""
    if not user.password:
        raise InvalidCredentialsError(message="User has no password set.")
    hashed_password = user.password
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_access_token(data: dict) -> str:
    """Create A New Jwt Access Token"""
    to_encode = data.copy()

    expire = datetime.now(
        timezone.utc) + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, config.SECRET_KEY, config.ALGORITHM)  # returns a token
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """Create A New Jwt Refresh Token"""
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + \
        timedelta(days=config.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, config.SECRET_KEY, config.ALGORITHM)  # returns a token
    return encoded_jwt


def verify_access_token(token: str, credential_exceptions: Exception) -> dict:
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, config.SECRET_KEY,
                             algorithms=[config.ALGORITHM])
        if payload is None:
            raise credential_exceptions
        return payload

    except JWTError as exc:
        raise credential_exceptions from exc


# def create_refresh_tokens(refresh_token: str, credential_exceptions) -> TokenResponse:
#     """Create a new access token and refresh token"""
#     payload = verify_access_token(
#         refresh_token, credential_exceptions)
#     new_access_token = create_access_token(payload)
#     new_refresh_token = create_refresh_token(payload)
#     return TokenResponse(access_token=new_access_token, refresh_token=new_refresh_token, token_type="Bearer")


def retrive_token(user) -> str:
    """Return Access and Refresh Tokens"""
    data = {"user_id": user.id,
            "user_role": user.role,
            "organization_id": user.organization_id,
            }
    access_token = create_access_token(data)
    # refresh_token = create_refresh_token(data)
    return access_token
