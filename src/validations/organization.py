from src.core.exceptions import PermissionDeniedError, EntityNotFoundError


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
