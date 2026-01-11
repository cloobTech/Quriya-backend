from src.core.exceptions import EntityNotFoundError
from src.utils.fetch_or_exists import fetch_or_exists
from src.core.exceptions import EntityNotFoundError, InvalidCoverageSelectionError
from src.schemas.project_coverage import CoverageSelection


async def validate_existence(repo, ids: set[str], entity: str):
    if not ids:
        return

    existing_ids = await repo

    missing = ids - existing_ids
    if missing:
        raise EntityNotFoundError(
            message=f"{entity} not found",
            details={"ids": list(missing)},
        )


async def validate_project_exists(
    repo,
    project_id: str
) -> None:
    """Validate project exists"""
    if not await fetch_or_exists(repo,
                                 id=project_id,
                                 only_exists=True):
        raise EntityNotFoundError(
            message="Election project not found",
            details={"project_id": project_id}
        )


def validate_coverage_selection(data: CoverageSelection) -> None:
    """Validate that at least one coverage level is selected"""
    if not any([
        data.state_ids,
        data.lga_ids,
        data.ward_ids,
        data.polling_unit_ids,
    ]):
        raise InvalidCoverageSelectionError(message="At least one coverage level [state, "
                                            "lga, ward or pu] must be selected")


async def validate_location_existence(repo, ids: list[str]) -> set[str]:
    """verify that the Id of a location (e.g. Lagos) is in our db """
    validated_ids = await repo.get_existing_ids(set(ids))
    if not validated_ids:
        raise InvalidCoverageSelectionError(message="Location Id not found in our database", details={
            "ids": f"{ids}"
        })
    return validated_ids
