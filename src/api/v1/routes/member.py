# from fastapi.routing import APIRouter
from fastapi import Depends, APIRouter
from src.api.v1.dependencies import get_uow, require_role_in_org
from src.models.enums import ElectionRole, UserRole
from src.services.project_member import ProjectMemberService
from src.schemas.project_member import AddMultipleProjectMembers, AgentQueryParams
from src.unit_of_work.unit_of_work import UnitOfWork
from src.models.user import User
from src.schemas.default import PaginationParams, PaginatedResponse


router = APIRouter()

ADMIN = require_role_in_org(UserRole.ORG_ADMIN)


# Project Members
@router.post("/members", response_model=dict)
async def add_members_to_project(project_id: str, data: AddMultipleProjectMembers, uow: UnitOfWork = Depends(get_uow), current_user: User = Depends(ADMIN)):
    """Add members to election project"""
    member_service = ProjectMemberService(uow)
    created_members = await member_service.add_members_to_election_project(data=data, project_id=project_id)
    return {
        "message": "Member(s) added to election project",
        "members": [member.to_dict() for member in created_members]
    }


@router.get("/members", response_model=dict)
async def get_project_members(project_id: str, role: ElectionRole | None = None, uow: UnitOfWork = Depends(get_uow),
                              current_user: User = Depends(ADMIN)):
    """Get project members"""
    member_service = ProjectMemberService(uow)
    members = await member_service.get_project_members(project_id=project_id, role=role)
    return {
        "message": "Project members",
        "members": members
    }


# AGENTS
@router.get("/agents", response_model=PaginatedResponse)
async def get_agents_with_assignments_and_location(project_id: str, uow: UnitOfWork = Depends(get_uow),
                                                   current_user: User = Depends(ADMIN), pagination: PaginationParams = Depends(), filters: AgentQueryParams = Depends()):
    """Get project members"""
    print("Filters:", filters)
    print("Filters:", filters.lga_id)
    print("Pagination:", pagination)
    print(pagination.page_size)
    member_service = ProjectMemberService(uow)
    members = await member_service.get_agents_with_assignments_and_location(project_id=project_id, pagination=pagination, filters=filters)
    return members


@router.get("/agents/statistics", response_model=dict)
async def get_agent_statistics(project_id: str, uow: UnitOfWork = Depends(get_uow), current_user: User = Depends(ADMIN)):
    """Get project members"""
    member_service = ProjectMemberService(uow)
    stats = await member_service.get_agent_statistics(project_id=project_id)
    return {
        "message": "Agent statistics",
        "statistics": stats
    }
