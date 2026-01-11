from src.unit_of_work.unit_of_work import UnitOfWork
from src.core.exceptions import EntityNotFoundError


class StateService:
    def __init__(self, uow_factory: UnitOfWork) -> None:
        self.uow_factory = uow_factory

    async def get_all_states(self):
        async with self.uow_factory as uow:
            states = await uow.state_repo.get_all()
            return list(states)

    async def get_state_by_id(self, state_id: str):
        async with self.uow_factory as uow:
            try:
                state = await uow.state_repo.get_by_id(state_id)
                if state is None:
                    raise EntityNotFoundError(
                        message=f"State with id {state_id} not found")
                return state
            except Exception as e:
                raise EntityNotFoundError(message=str(e))
