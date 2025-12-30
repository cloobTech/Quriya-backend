import csv
import uuid
from contextlib import asynccontextmanager
from sqlalchemy import select
from src.models.state import State
from src.models.local_government_area import LGA
from src.models.ward import Ward
from src.models.polling_unit import PollingUnit
from src.storage import db
import asyncio


def normalize(value: str | None) -> str | None:
    if not value:
        return None
    return " ".join(value.strip().split())


async def import_polling_units(csv_path: str):
    state_cache: dict[str, str] = {}
    lga_cache: dict[tuple[str, str], str] = {}
    ward_cache: dict[tuple[str, str], str] = {}

    async with db.get_session() as session:
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                state_name = normalize(row["state_name"])
                lga_name = normalize(row["local_government_name"])
                ward_name = normalize(row["ward_name"])
                pu_name = normalize(row["name"])

                if not all([state_name, lga_name, ward_name, pu_name]):
                    continue

                lat = row.get("location.latitude")
                lng = row.get("location.longitude")

                # ---------- STATE ----------
                if state_name and state_name not in state_cache:
                    result = await session.execute(
                        select(State).where(State.name == state_name)
                    )
                    state = result.scalar_one_or_none()

                    if not state:
                        state = State(

                            name=state_name,
                        )
                        session.add(state)
                        await session.flush()

                    if state_name:  # Ensure state_name is not None
                        state_cache[state_name] = state.id

                state_id = state_cache[state_name] if state_name else None

                # ---------- LGA ----------
                lga_key = (state_id, lga_name) if state_id and lga_name else None
                if state_id and lga_name:  # Ensure both are not None
                    lga_key = (state_id, lga_name)
                    if lga_key not in lga_cache:
                        result = await session.execute(
                            select(LGA).where(
                                LGA.name == lga_name,
                                LGA.state_id == state_id,
                            )
                        )
                        lga = result.scalar_one_or_none()

                        if not lga:
                            lga = LGA(

                                name=lga_name,
                                state_id=state_id,
                            )
                            session.add(lga)
                            await session.flush()

                        lga_cache[lga_key] = lga.id

                lga_id = lga_cache[lga_key] if lga_key in lga_cache else None

                # ---------- WARD ----------
                ward_key = (lga_id, ward_name) if lga_id and ward_name else None
                if ward_key and ward_key not in ward_cache:
                    result = await session.execute(
                        select(Ward).where(
                            Ward.name == ward_name,
                            Ward.lga_id == lga_id,
                        )
                    )
                    ward = result.scalar_one_or_none()

                    if not ward:
                        ward = Ward(

                            name=ward_name,
                            lga_id=lga_id,
                        )
                        session.add(ward)
                        await session.flush()

                    ward_cache[ward_key] = ward.id

                ward_id = ward_cache[ward_key] if ward_key else None

                # ---------- POLLING UNIT ----------
                result = await session.execute(
                    select(PollingUnit).where(
                        PollingUnit.name == pu_name,
                        PollingUnit.ward_id == ward_id,
                    )
                )
                exists = result.scalar_one_or_none()

                if not exists:
                    session.add(
                        PollingUnit(

                            name=pu_name,
                            ward_id=ward_id,
                            latitude=float(lat) if lat else None,
                            longitude=float(lng) if lng else None,
                            location_source="google_places"
                            if lat and lng
                            else None,
                        )
                    )

        await session.commit()


import asyncio

asyncio.run(import_polling_units("/home/cloobtech/Projects/inec-polling-units/polling-units.csv"))