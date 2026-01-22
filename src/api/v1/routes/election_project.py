from fastapi import APIRouter, Depends
from src.api.v1.dependencies import get_uow, require_role_in_org
from src.schemas.election_project import CreateProject
from src.schemas.project_assignment import AssignPollingUnitToProjectMember
from src.models.user import User
from src.models.enums import UserRole
from src.services.project import ProjectService
from src.services.project_assignment import ProjectAssignmentService
from src.unit_of_work.unit_of_work import UnitOfWork


router = APIRouter()

ADMIN = require_role_in_org(UserRole.ORG_ADMIN)


@router.get("/", response_model=dict)
async def get_organization_monitoring_projects(current_user: User = Depends(ADMIN), uow: UnitOfWork = Depends(get_uow)):
    election_project_service = ProjectService(uow)
    projects = await election_project_service.get_organization_projects(organization_id=current_user.organization_id)
    return {
        "projects": [project.to_dict() for project in projects],
        "message": "Election monitoring projects"}


@router.get("/{project_id}", response_model=dict)
async def get_organization_monitoring_project(project_id: str, current_user: User = Depends(ADMIN), uow: UnitOfWork = Depends(get_uow)):
    election_project_service = ProjectService(uow)
    project = await election_project_service.get_organization_project(project_id=project_id)
    return {
        "project": project.to_dict(),
        "message": "Election monitoring project"}


@router.post("/", response_model=dict)
async def create_election_monitoring_project(data: CreateProject, uow: UnitOfWork = Depends(get_uow), current_user: User = Depends(ADMIN)):
    """Create a new election monitoring project"""

    election_project_service = ProjectService(uow)
    new_project = await election_project_service.create_election_monitoring_project(data=data, createdby_user_id=current_user.id, organization_id=current_user.organization_id)
    return {
        "message": "New election monitoring project created",
        "project": new_project.to_dict()
    }


# Project Assignments


@router.post("/{project_id}/assignments", response_model=dict)
async def assign_polling_units_to_project_members(project_id: str, data: AssignPollingUnitToProjectMember, uow: UnitOfWork = Depends(get_uow), current_user: User = Depends(ADMIN)):
    """Assign polling units to project members"""
    assignment_service = ProjectAssignmentService(uow)

    assignments = await assignment_service.assign_polling_units_to_project_member(
        data=data, project_id=project_id
    )
    return {
        "message": "Polling units assigned to project member",
        "assignments": [assignment.to_dict() for assignment in assignments]
    }
