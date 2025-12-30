from fastapi import APIRouter, Depends
from src.schemas.result import SubmitResultSchema
from src.models.user import User
from src.services.result import ResultService
from src.api.v1.dependencies import get_current_user, get_uow
from src.unit_of_work.unit_of_work import UnitOfWork


router = APIRouter()


# FIELD_AGENT = require_role("FIELD_AGENT")


@router.post("", response_model=dict)
async def submit_result(
    project_id: str,
    result_data: SubmitResultSchema,
    current_user: User = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_uow),

):
    """Submit election result for a polling unit"""
    result_service = ResultService(uow)
    result = await result_service.submit_result(
        project_id=project_id,
        user_id=current_user.id,
        result_data=result_data
    )
    return {"message": "Result submitted successfully", "data": result.to_dict()}
