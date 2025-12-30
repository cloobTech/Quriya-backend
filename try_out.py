from src.storage import db
import asyncio
from src.repositories.project_state_coverage import StateCoverageRepository
from src.repositories.project_member import ProjectMemberRepository
from src.repositories.user import UserRepository
from src.models.user import User
from src.repositories.state import StateRepository
from src.auth.security import hash_password


async def get_id():
    async with db.get_session() as session:
        # state = StateCoverageRepository(session)
        # state = StateRepository(session)
        # user = UserRepository(session)
        # active_user: User | None = await user.get_by_id("db50e751-b8f7-40fe-9c42-f591ba232115")
        # pwd = "password"
        # hash_pwd = hash_password(pwd)
        # if active_user:
        #     active_user.password = hash_pwd

        # session.add(active_user)
        # await session.commit()

        member = ProjectMemberRepository(session)
        project_member = await member.get_member_by_user_id(
            user_id="db50e751-b8f7-40fe-9c42-f591ba232115",
            project_id="4c78111b-ab25-48ac-94bd-75d8e28c434f"
        )
        print(project_member)

        # result = await state.get_existing_ids("a29c8de7-2fcf-47eb-9225-49bc04fc06ba", ["b31a4230-35c0-46c9-8673-0bbdf2818ceb", "234"], "state_id")
        # result = await state.get_existing_ids(set(["b31a4230-35c0-46c9-8673-0bbdf2818ceb", "123"]))
        # print(result)


asyncio.run(get_id())
