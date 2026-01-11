from src.unit_of_work.unit_of_work import UnitOfWork
from src.core.exceptions import EntityNotFoundError
from src.models.ward import Ward


class WardService:
    def __init__(self, uow_factory: UnitOfWork) -> None:
        self.uow_factory = uow_factory

    async def get_all_wards(self) -> list[Ward]:
        async with self.uow_factory as uow:
            wards = await uow.ward_repo.get_all()
            return list(wards)

    async def get_ward_by_id(self, ward_id: str) -> Ward:
        async with self.uow_factory as uow:
            try:
                ward = await uow.ward_repo.get_by_id(ward_id)
                if ward is None:
                    raise EntityNotFoundError(
                        message=f"Ward with id {ward_id} not found")
                return ward
            except Exception as e:
                raise EntityNotFoundError(message=str(e))

    async def get_wards_by_lga_id(self, lga_id: str) -> list[Ward]:
        async with self.uow_factory as uow:
            wards = await uow.ward_repo.filter_by(lga_id=lga_id)
            return list(wards)
