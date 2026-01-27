from src.utils.fetch_or_exists import fetch_or_exists
from src.core.exceptions import EntityNotFoundError, PermissionDeniedError, DuplicateEntryError
from src.models.enums import ElectionRole, ResultStatus
from src.unit_of_work.unit_of_work import UnitOfWork


async def validate_pu_exists(
    uow: UnitOfWork,
    pu_id: str,
) -> None:
    """Validate that the polling unit exists in the project"""
    pu_exists = await fetch_or_exists(
        uow.pu_coverage_repo,
        id=pu_id,
        only_exists=True
    )
    if not pu_exists:
        raise EntityNotFoundError(message="Polling unit not found in the project", details={
                                  "pu_id": pu_id})


async def validate_authorized_user(
    uow,
    user_id: str,
    project_id: str,
    pu_id: str
) -> None:
    """Validate that the user is authorized to submit results for the project"""
    user_authorized = await uow.election_project_member_repo.get_member_by_user_id(
        user_id=user_id,
        project_id=project_id)

    if not user_authorized or user_authorized.role != ElectionRole.FIELD_AGENT:
        raise PermissionDeniedError(message="User not authorized for this project, "
                                    f"user has to be a {ElectionRole.FIELD_AGENT} attached to this polling unit",
                                    details={"user_id": user_id, "project_id": project_id, "pu_id": pu_id})


async def validate_result_not_exists(
    uow,
    project_id: str,
    pu_id: str
) -> None:
    """Validate that a result does not already exist for the polling unit in the project"""
    result_exists = await fetch_or_exists(
        uow,
        filter_by={
            "project_id": project_id,
            "polling_unit_id": pu_id
        },
        only_exists=True
    )
    if result_exists:
        raise DuplicateEntryError(message="Result already submitted for this polling unit in the project", details={
            "project_id": project_id, "pu_id": pu_id})


async def validate_pu_coverage(
    uow,
    project_id: str,
    pu_id: str
) -> None:
    """Validate that the polling unit is covered in the election project"""
    pu_covered = await fetch_or_exists(
        uow,
        filter_by={
            "project_id": project_id,
            "id": pu_id
        },
        only_exists=True
    )
    if not pu_covered:
        raise EntityNotFoundError(message="Polling unit not covered in the election project", details={
                                  "project_id": project_id, "id": pu_id})
