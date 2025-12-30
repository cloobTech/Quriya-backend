import asyncio
import json
from src.models.political_party import PoliticalParty
from src.storage import db


async def seed_parties():
    with open("nigerian_parties.json") as f:
        parties = json.load(f)

    async with db.get_session() as session:  # your AsyncSession
        for party in parties:
            exists = await session.scalar(
                PoliticalParty.__table__.select().where(
                    PoliticalParty.acronym == party["acronym"])
            )
            if exists:
                continue  # skip duplicates
            new_party = PoliticalParty(
                name=party["name"],
                acronym=party["acronym"],
                logo_url=party["logo_url"]
            )
            print("Seeding party:", new_party.acronym)
            session.add(new_party)
        await session.commit()
    print("Nigerian parties seeded successfully!")

# Usage:
asyncio.run(seed_parties())
