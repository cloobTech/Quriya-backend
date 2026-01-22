from fastapi import APIRouter, Depends
from src.api.v1.dependencies import get_uow, require_role_in_org
from src.schemas.project_coverage import (CoverageSelection,
                                          StateCoverageOut, LGAOut, WardOut, PollingUnitOut)
from src.services.project_coverage import ProjectCoverageService
from src.unit_of_work.unit_of_work import UnitOfWork
from src.models.enums import UserRole
from src.models.user import User


router = APIRouter()
ADMIN = require_role_in_org(UserRole.ORG_ADMIN)


# Project Coverage
@router.post("", response_model=dict)
async def select_coverage_locations(project_id: str, data: CoverageSelection, uow: UnitOfWork = Depends(get_uow), current_user: User = Depends(ADMIN)):
    """Select coverage locations for election project"""
    coverage_service = ProjectCoverageService(uow)
    response = await coverage_service.select_project_coverage_locations(data=data, project_id=project_id)
    return response


@router.get("/states", response_model=dict)
async def get_state_coverage(project_id: str, uow: UnitOfWork = Depends(get_uow), current_user: User = Depends(ADMIN)):
    coverage_service = ProjectCoverageService(uow)
    response = await coverage_service.get_state_coverage(project_id=project_id)

    return {
        "message": "State coverage",
        "state_coverage": [
            StateCoverageOut.model_validate(coverage) for coverage in response
        ]
    }


@router.get("/lgas", response_model=dict)
async def get_lga_coverage(project_id: str,  state_coverage_id: str, uow: UnitOfWork = Depends(get_uow), current_user: User = Depends(ADMIN)):
    coverage_service = ProjectCoverageService(uow)
    response = await coverage_service.get_lga_coverage_by_state_id(project_id=project_id, state_coverage_id=state_coverage_id)

    return {
        "message": "LGA coverage",
        "lga_coverage": [
            LGAOut.model_validate(coverage) for coverage in response
        ]
    }


@router.get("/wards", response_model=dict)
async def get_ward_coverage(project_id: str, lga_coverage_id: str, uow: UnitOfWork = Depends(get_uow), current_user: User = Depends(ADMIN)):
    coverage_service = ProjectCoverageService(uow)
    response = await coverage_service.get_ward_coverage_by_lga_id(project_id=project_id, lga_coverage_id=lga_coverage_id)

    return {
        "message": "Ward coverage",
        "ward_coverage": [
            WardOut.model_validate(coverage) for coverage in response
        ]
    }


@router.get("/polling-units", response_model=dict)
async def get_pu_coverage(project_id: str, ward_coverage_id: str, assigned_status: bool | None = None, uow: UnitOfWork = Depends(get_uow), current_user: User = Depends(ADMIN)):
    coverage_service = ProjectCoverageService(uow)
    response = await coverage_service.get_pu_coverage_by_ward_id(project_id=project_id, ward_coverage_id=ward_coverage_id, assigned_status=assigned_status)

    return {
        "message": "PU coverage",
        "pu_coverage": [
            PollingUnitOut.model_validate(coverage) for coverage in response
        ]
    }
