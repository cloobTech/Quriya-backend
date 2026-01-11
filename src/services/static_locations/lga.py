from src.unit_of_work.unit_of_work import UnitOfWork
from src.core.exceptions import EntityNotFoundError


class LgaService:
    def __init__(self, uow_factory: UnitOfWork) -> None:
        self.uow_factory = uow_factory

    async def get_all_lgas(self):
        async with self.uow_factory as uow:
            lgas = await uow.lga_repo.get_all()
            return list(lgas)

    async def get_lga_by_id(self, lga_id: str):
        async with self.uow_factory as uow:
            try:
                lga = await uow.lga_repo.get_by_id(lga_id)
                if lga is None:
                    raise EntityNotFoundError(
                        message=f"LGA with id {lga_id} not found")
                return lga
            except Exception as e:
                raise EntityNotFoundError(message=str(e))

    async def get_lgas_by_state_id(self, state_id: str):
        async with self.uow_factory as uow:
            lgas = await uow.lga_repo.filter_by(state_id=state_id)
            return list(lgas)