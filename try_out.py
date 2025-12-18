from src.storage import db
import asyncio
from src.repositories.project_state_coverage import StateCoverageRepository
from src.repositories.state import StateRepository


async def get_id():
    async with db.get_session() as session:
        # state = StateCoverageRepository(session)
        state = StateRepository(session)

        # result = await state.get_existing_ids("a29c8de7-2fcf-47eb-9225-49bc04fc06ba", ["b31a4230-35c0-46c9-8673-0bbdf2818ceb", "234"], "state_id")
        result = await state.get_existing_ids(set(["b31a4230-35c0-46c9-8673-0bbdf2818ceb", "123"]))
        print(result)


asyncio.run(get_id())
