from fastapi import APIRouter, Depends
from src.api.v1.dependencies import get_uow, require_role
from src.schemas.election import CreateElectionProject
from src.models.user import User
from src.services.election_project import ElectionProjectService
from src.unit_of_work.unit_of_work import UnitOfWork
from src.schemas.user import UserRole


router = APIRouter()

ADMIN = require_role(UserRole.ORG_ADMIN)


@router.post("/", response_model=dict)
async def create_organization(data: CreateElectionProject, uow: UnitOfWork = Depends(get_uow), current_user: User = Depends(ADMIN),):
    election_project_service = ElectionProjectService(uow)
    new_project = await election_project_service.create_election_monitoring_project(data)
    return {
        "message": "New election monitoring project created",
        "project": new_project.to_dict()
    }
