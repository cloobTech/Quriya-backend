from fastapi import APIRouter, Depends
from src.api.v1.dependencies import get_uow, require_role_in_org
from src.schemas.election_project import CreateProject
from src.schemas.election_project_member import AddMultipleProjectMembers
from src.schemas.project_assignment import AssignPollingUnitToProjectMember
from src.schemas.project_coverage import CoverageSelection
from src.schemas.user import UserRole
from src.models.user import User
from src.services.election_project import ProjectService
from src.services.project_coverage import ProjectCoverageService
from src.services.election_project_member import ProjectMemberService
from src.services.project_assignment import ProjectAssignmentService
from src.unit_of_work.unit_of_work import UnitOfWork


router = APIRouter()

ADMIN = require_role_in_org(UserRole.ORG_ADMIN)


@router.post("/", response_model=dict)
async def create_election_monitoring_project(data: CreateProject, uow: UnitOfWork = Depends(get_uow), current_user: User = Depends(ADMIN)):
    """Create a new election monitoring project"""

    election_project_service = ProjectService(uow)
    new_project = await election_project_service.create_election_monitoring_project(data=data, createdby_user_id=current_user.id, organization_id=current_user.organization_id)
    return {
        "message": "New election monitoring project created",
        "project": new_project.to_dict()
    }


@router.post("/{project_id}/coverage", response_model=dict)
async def select_coverage_locations(project_id: str, data: CoverageSelection, uow: UnitOfWork = Depends(get_uow), current_user: User = Depends(ADMIN)):
    """Select coverage locations for election project"""
    coverage_service = ProjectCoverageService(uow)
    response = await coverage_service.select_project_coverage_locations(data=data, project_id=project_id)
    return response


@router.post("/{project_id}/members", response_model=dict)
async def add_members_to_project(project_id: str, data: AddMultipleProjectMembers, uow: UnitOfWork = Depends(get_uow), current_user: User = Depends(ADMIN)):
    """Add members to election project"""
    member_service = ProjectMemberService(uow)
    created_members = await member_service.add_members_to_election_project(data=data, project_id=project_id)
    return {
        "message": "Member(s) added to election project",
        "members": [member.to_dict() for member in created_members]
    }


@router.post("/{project_id}/assignments", response_model=dict)
async def assign_polling_units_to_project_members(project_id: str, data: AssignPollingUnitToProjectMember, uow: UnitOfWork = Depends(get_uow), current_user: User = Depends(ADMIN)):
    """Assign polling units to project members"""
    assignment_service = ProjectAssignmentService(uow)

    assignments = await assignment_service.assign_polling_units_to_project_member(
        data=data, project_id=project_id
    )
    return {
        "message": "Polling units assigned to project members",
        "assignments": [assignment.to_dict() for assignment in assignments]
    }
