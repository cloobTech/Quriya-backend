from fastapi import APIRouter, Depends
from src.api.v1.dependencies import get_uow
from src.services.organization import OrganizationService
from src.schemas.organization import CreateOrganizationWithAdmin
from src.unit_of_work.unit_of_work import UnitOfWork


router = APIRouter()


# @router.post("/", response_model=dict)
# async def create_organization(org: CreateOrganizationWithAdmin, uow: UnitOfWork = Depends(get_uow)):
#     org_service = OrganizationService(uow)
#     new_org, admin_user = await org_service.create_organization_with_admin(
#         org.organization, org.admin_user
#     )
#     return {
#         "message": "Organization created",
#         "organization_id": new_org.id,
#         "admin_user_id": admin_user.id
#     }
