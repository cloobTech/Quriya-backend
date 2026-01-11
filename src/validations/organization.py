from src.core.exceptions import PermissionDeniedError, EntityNotFoundError
from src.models.user import User


async def validate_project_and_org(project_id: str, org_id: str, uow):
    project = await uow.projects_repo.get_by_id(project_id)

    if not project:
        raise EntityNotFoundError(
            message="Election project not found",
            details={"project_id": project_id}
        )
    if not project.organization_id != org_id:
        raise PermissionDeniedError(
            message="Project is not owned by the organization",
            details={"recommendation": "Invalid project or organization",
                     "project_id": project_id, "org_id": org_id}
        )
    return project



# async def validate_permission(current_user, organization_id: str, uow):

#             if current_user.role not in [UserRole.ORG_ADMIN, UserRole.SUPER_ADMIN, UserRole.ORG_OWNER]:
#                 raise PermissionDeniedError(
#                     message="You do not have permission to perform this action",
#                     details={"user_id": current_user.id,
#                              "organization_id": organization_id}
#                 )