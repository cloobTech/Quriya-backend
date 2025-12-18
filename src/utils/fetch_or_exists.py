from src.core.exceptions import EntityNotFoundError


async def fetch_or_exists(
    repo,
    *,
    id: str | None = None,
    filter_by: dict | None = None,
    message: str | None = None,
    details: dict | None = None,
    only_exists: bool = False
):
    """
    Universal helper:
     - If only_exists=True → return True/False
     - Else → fetch entity or raise EntityNotFoundError
    """

    # Decide how to query
    if id is not None:
        entity = await repo.get_by_id(id)
    else:
        entity = await repo.exists(**(filter_by or {}))

    # If we are only validating existence
    if only_exists:
        return bool(entity)

    # If fetching and it doesn't exist
    if not entity:
        model_name = getattr(repo, "model", repo.__class__.__name__)
        if message is None:
            message = f"{model_name} not found"
        raise EntityNotFoundError(message=message, details=details)

    return entity
