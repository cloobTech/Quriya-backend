from fastapi import APIRouter, Depends
from src.api.v1.dependencies import get_current_user, get_user_service, require_role
from src.services.user import UserService
from src.models.user import User
from src.schemas.user import CreateUser
from src.schemas.user import UserRole


router = APIRouter()

ADMIN = require_role(UserRole.ORG_ADMIN)


@router.get("/me", response_model=dict)
async def get_user_profile(current_user: User = Depends(get_current_user), user_service: UserService = Depends(get_user_service)):
    """Return user's profile"""
    user, org = await user_service.user_profile(current_user.id)
    return {"user": user.to_dict(),
            "organization": org.to_dict()
            }


@router.post("/", response_model=dict)
async def create_user(user_data: CreateUser, current_user: User = Depends(ADMIN), user_service: UserService = Depends(get_user_service)):
    """Create new user"""
    user_data.admin_organization_id = current_user.organization_id
    new_user = await user_service.create_user(user_data)
    return new_user.to_dict()
