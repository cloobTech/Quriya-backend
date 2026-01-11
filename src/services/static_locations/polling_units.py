from src.unit_of_work.unit_of_work import UnitOfWork
from src.core.exceptions import EntityNotFoundError


class PollingUnitService:
    def __init__(self, uow_factory: UnitOfWork) -> None:
        self.uow_factory = uow_factory

    async def get_all_polling_units(self):
        async with self.uow_factory as uow:
            polling_units = await uow.polling_unit_repo.get_all()
            return list(polling_units)

    async def get_polling_unit_by_id(self, polling_unit_id: str):
        async with self.uow_factory as uow:
            try:
                polling_unit = await uow.polling_unit_repo.get_by_id(polling_unit_id)
                if polling_unit is None:
                    raise EntityNotFoundError(
                        message=f"Polling Unit with id {polling_unit_id} not found")
                return polling_unit
            except Exception as e:
                raise EntityNotFoundError(message=str(e))

    async def get_polling_units_by_ward_id(self, ward_id: str):
        async with self.uow_factory as uow:
            polling_units = await uow.polling_unit_repo.filter_by(ward_id=ward_id)
            return list(polling_units)
