from fastapi import APIRouter, Depends, Path
from src.api.v1.dependencies import get_current_user, get_user_service, require_role_in_org, validate_organization_route
from src.services.user import UserService
from src.models.user import User
from src.schemas.user import CreateUser
from src.schemas.user import UserRole


router = APIRouter()

ADMIN = require_role_in_org(UserRole.ORG_ADMIN)


@router.get("/me", response_model=dict)
async def get_user_profile(organization_id: str = Path(...), current_user: User = Depends(get_current_user),
                           user_service: UserService = Depends(get_user_service), validate_organization_route=Depends(validate_organization_route)):
    """Return user's profile"""
    user, org = await user_service.user_profile(current_user.id)
    return {"user": user.to_dict(),
            "organization": org.to_dict()
            }


@router.post("/", response_model=dict)
async def create_users(user_data: list[CreateUser], organization_id: str = Path(...), current_user: User = Depends(ADMIN),
                       user_service: UserService = Depends(get_user_service), validate_organization_route=Depends(validate_organization_route)):
    """Create new user"""
    new_users = await user_service.create_users(user_data, created_by=current_user)

    return {"message": f"{len(new_users)} Users created successfully"}
