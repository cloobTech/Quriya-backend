from fastapi import APIRouter, Depends
from src.api.v1.dependencies import get_uow
from src.services.static_locations.state import StateService
from src.services.static_locations.lga import LgaService
from src.services.static_locations.ward import WardService
from src.services.static_locations.polling_units import PollingUnitService
from src.unit_of_work.unit_of_work import UnitOfWork
from src.schemas.locations import (StateResponse, LgaResponse,
                                   WardResponse, PollingUnitResponse)

router = APIRouter()


# States
@router.get("/states", response_model=list[StateResponse])
async def get_states(uow: UnitOfWork = Depends(get_uow)):
    location_service = StateService(uow)
    states = await location_service.get_all_states()
    return [
        StateResponse.model_validate(state) for state in states
    ]


@router.get("/states/{state_id}", response_model=StateResponse)
async def get_state_by_id(state_id: str, uow: UnitOfWork = Depends(get_uow)):
    location_service = StateService(uow)
    state = await location_service.get_state_by_id(state_id)
    return StateResponse.model_validate(state)


# LGA
@router.get("/lgas", response_model=list[LgaResponse])
async def get_lgas_by_state_id(state_id: str, uow: UnitOfWork = Depends(get_uow)):
    location_service = LgaService(uow)
    lgas = await location_service.get_lgas_by_state_id(state_id)
    return [
        LgaResponse.model_validate(lga) for lga in lgas
    ]


@router.get("/lgas/{lga_id}", response_model=LgaResponse)
async def get_lga_by_id(lga_id: str, uow: UnitOfWork = Depends(get_uow)):
    location_service = LgaService(uow)
    lga = await location_service.get_lga_by_id(lga_id)
    return LgaResponse.model_validate(lga)


# Ward
@router.get("/wards", response_model=list[WardResponse])
async def get_wards_by_lga_id(lga_id: str, uow: UnitOfWork = Depends(get_uow)):
    location_service = WardService(uow)
    wards = await location_service.get_wards_by_lga_id(lga_id)
    return [
        WardResponse.model_validate(ward) for ward in wards
    ]


@router.get("/wards/{ward_id}", response_model=WardResponse)
async def get_ward_by_id(ward_id: str, uow: UnitOfWork = Depends(get_uow)):
    location_service = WardService(uow)
    ward = await location_service.get_ward_by_id(ward_id)
    return WardResponse.model_validate(ward)

# Polling Unit


@router.get("/polling-units", response_model=list[PollingUnitResponse])
async def get_polling_units_by_ward_id(ward_id: str, uow: UnitOfWork = Depends(get_uow)):
    location_service = PollingUnitService(uow)
    polling_units = await location_service.get_polling_units_by_ward_id(ward_id)
    return [
        PollingUnitResponse.model_validate(polling_unit) for polling_unit in polling_units
    ]


@router.get("/polling-units/{polling_unit_id}", response_model=PollingUnitResponse)
async def get_polling_unit_by_id(polling_unit_id: str, uow: UnitOfWork = Depends(get_uow)):
    location_service = PollingUnitService(uow)
    polling_unit = await location_service.get_polling_unit_by_id(polling_unit_id)
    return PollingUnitResponse.model_validate(polling_unit)
