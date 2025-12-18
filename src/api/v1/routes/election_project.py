from fastapi import APIRouter, Depends
from src.api.v1.dependencies import get_uow, require_role
from src.schemas.election_project import CreateElectionProject
from src.schemas.project_coverage import CoverageSelection
from src.schemas.user import UserRole
from src.models.user import User
from src.services.election_project import ElectionProjectService
from src.services.project_coverage import ProjectCoverageService
from src.unit_of_work.unit_of_work import UnitOfWork


router = APIRouter()

ADMIN = require_role(UserRole.ORG_ADMIN)


@router.post("/", response_model=dict)
async def create_organization(data: CreateElectionProject, uow: UnitOfWork = Depends(get_uow), current_user: User = Depends(ADMIN)):

    election_project_service = ElectionProjectService(uow)
    new_project = await election_project_service.create_election_monitoring_project(data=data, createdby_user_id=current_user.id, organization_id=current_user.organization_id)
    return {
        "message": "New election monitoring project created",
        "project": new_project.to_dict()
    }


@router.post("/{project_id}/coverage", response_model=dict)
async def select_coverage_locations(project_id: str, data: CoverageSelection, uow: UnitOfWork = Depends(get_uow), current_user: User = Depends(ADMIN)):
    coverage_service = ProjectCoverageService(uow)
    response = await coverage_service.select_project_coverage_locations(data=data, project_id=project_id)
    return response
