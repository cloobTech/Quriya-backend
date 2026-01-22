from src.unit_of_work.unit_of_work import UnitOfWork
from src.schemas.project_coverage import CoverageSelection
from src.models.project_state_coverage import ProjectStateCoverage
from src.models.project_lga_coverage import ProjectLgaCoverage
from src.models.project_ward_coverage import ProjectWardCoverage
from src.models.project_pu_coverage import ProjectPuCoverage
from src.validations.coverage import (validate_project_exists,
                                      validate_coverage_selection, validate_location_existence)
from src.repositories.project_state_coverage import StateCoverageRepository
from src.repositories.project_lga_coverage import LgaCoverageRepository
from src.repositories.project_ward_coverage import WardCoverageRepository
from src.repositories.project_pu_coverage import PuCoverageRepository


class ProjectCoverageService:
    """The locations a project intends to monitor"""

    def __init__(self, uow_factory: UnitOfWork) -> None:
        self.uow_factory = uow_factory

    async def select_project_coverage_locations(self, data: CoverageSelection, project_id: str):
        """select state(s), ward(s), lga(s) and PU(s) a project intends to monitors"""

        validate_coverage_selection(data)

        async with self.uow_factory as uow:
            # await self._validate_project_exists(uow, project_id)
            await validate_project_exists(uow.election_project_repo, project_id)
            stats = {

            }

            # State
            validated_state_ids = await validate_location_existence(repo=uow.state_repo, ids=data.state_ids)
            state_coverage_map, state_count = await self.bulk_create_state_coverage(
                repo=uow.state_coverage_repo,
                project_id=project_id,
                state_ids=validated_state_ids,
            )

            # LGA
            validated_lga_ids = await validate_location_existence(repo=uow.lga_repo, ids=data.lga_ids)
            lga_state_map = await uow.lga_repo.get_state_ids_for_lgas(validated_lga_ids)
            lga_coverage_map, lga_count = await self.bulk_create_lga_coverage(
                repo=uow.lga_coverage_repo,
                project_id=project_id,
                lga_state_map=lga_state_map,
                state_coverage_map=state_coverage_map
            )

            # Ward
            validated_ward_ids = await validate_location_existence(repo=uow.ward_repo, ids=data.ward_ids)
            ward_lga_map = await uow.ward_repo.get_lga_ids_for_wards(validated_ward_ids)
            ward_coverage_map, ward_count = await self.bulk_create_ward_coverage(
                repo=uow.ward_coverage_repo,
                project_id=project_id,
                ward_lga_map=ward_lga_map,
                lga_coverage_map=lga_coverage_map
            )

            # PUs
            validated_pu_ids = await validate_location_existence(repo=uow.polling_unit_repo, ids=data.polling_unit_ids)
            pu_ward_map = await uow.polling_unit_repo.get_ward_ids_for_pus(validated_pu_ids)

            pu_coverage_map, len_of_pus = await self.bulk_create_pu_coverage(
                repo=uow.pu_coverage_repo,
                project_id=project_id,
                pu_ward_map=pu_ward_map,
                ward_coverage_map=ward_coverage_map
            )

            return {
                "message": "Coverages created successfully",
                "stats": {
                    "states_created": state_count,
                    "lgas_created": lga_count,
                    "wards_created": ward_count,
                    "pus_created": len_of_pus
                }
            }

    # inside State

    async def bulk_create_state_coverage(
        self,
        repo: StateCoverageRepository,
        project_id: str,
        state_ids: set[str],
    ):
        """
        Ensure ProjectStateCoverage exists for each state_id.
        Returns mapping { state_id: project_state_coverage_id }.
        """
        if not state_ids:
            return {}

        # 1. Fetch existing coverage
        existing_map = await repo.get_existing_by_state_ids(
            project_id, state_ids
        )

        # 2. Determine which states are missing
        missing_state_ids = state_ids - set(existing_map.keys())

        # 3. Create missing rows
        records = [
            ProjectStateCoverage(
                project_id=project_id,
                state_id=state_id,
            )
            for state_id in missing_state_ids
        ]

        if records:
            await repo.bulk_create(records)

        # 4. Re-fetch full mapping (existing + newly created)
        full_map = await repo.get_existing_by_state_ids(
            project_id, state_ids
        )

        return full_map, len(records)

    async def bulk_create_lga_coverage(
        self,
        repo: LgaCoverageRepository,
        project_id: str,
        lga_state_map: dict[str, str],
        state_coverage_map: dict[str, str],
    ):
        """
        Ensure ProjectLgaCoverage exists for every lga in lga_state_map.
        Returns mapping { lga_id: project_lga_coverage_id } (includes existing + newly created).
        """
        if not lga_state_map:
            return {}

        requested_lga_ids = set(lga_state_map.keys())

        # map of already-existing lga -> coverage_id
        existing_map = await repo.get_existing_by_lga_ids(project_id, requested_lga_ids)

        # Determine which lgas are new
        new_lga_ids = requested_lga_ids - set(existing_map.keys())

        records = []
        for lga_id in new_lga_ids:
            state_id = lga_state_map.get(lga_id)
            if not state_id:
                # no parent state found — skip or log; we don't want a FK violation
                continue
            state_cov_id = state_coverage_map.get(state_id)
            if not state_cov_id:
                # no parent coverage found — skip or log; we don't want a FK violation
                continue
            records.append(
                ProjectLgaCoverage(
                    project_id=project_id,
                    lga_id=lga_id,
                    state_coverage_id=state_cov_id
                )
            )

        if records:
            # repo.bulk_create should insert all records (and commit if your UoW does)
            await repo.bulk_create(records)

        # query again for a complete mapping (existing + newly created)
        full_map = await repo.get_existing_by_lga_ids(project_id, requested_lga_ids)
        return full_map, len(records)

    # WARD
    async def bulk_create_ward_coverage(
        self,
        repo: WardCoverageRepository,
        project_id: str,
        ward_lga_map: dict[str, str],
        lga_coverage_map: dict[str, str],
    ):
        """
        Ensure ProjectWardCoverage exists for every ward in ward_lga_map.
        Returns mapping { ward_id: project_ward_coverage_id } (includes existing + newly created).
        """
        if not ward_lga_map:
            return {}

        requested_ward_ids = set(ward_lga_map.keys())

        # map of already-existing ward -> coverage_id
        existing_map = await repo.get_existing_by_ward_ids(project_id, requested_ward_ids)

        # Determine which wards are new
        new_ward_ids = requested_ward_ids - set(existing_map.keys())

        records = []
        for ward_id in new_ward_ids:
            lga_id = ward_lga_map.get(ward_id)
            if not lga_id:
                # no parent lga found — skip or log; we don't want a FK violation
                continue
            lga_cov_id = lga_coverage_map.get(lga_id)
            if not lga_cov_id:
                # no parent coverage found — skip or log; we don't want a FK violation
                continue
            records.append(
                ProjectWardCoverage(
                    project_id=project_id,
                    ward_id=ward_id,
                    lga_coverage_id=lga_cov_id
                )
            )

        if records:
            # repo.bulk_create should insert all records (and commit if your UoW does)
            await repo.bulk_create(records)

        # query again for a complete mapping (existing + newly created)
        full_map = await repo.get_existing_by_ward_ids(project_id, requested_ward_ids)
        return full_map, len(records)

    # PU
    async def bulk_create_pu_coverage(
        self,
        repo: PuCoverageRepository,
        project_id: str,
        pu_ward_map: dict[str, str],
        ward_coverage_map: dict[str, str],
    ):
        """
        Ensure ProjectWardCoverage exists for every pu in pu_ward_map.
        Returns mapping { pu_id: project_pu_coverage_id } (includes existing + newly created).
        """
        if not pu_ward_map:
            return {}

        requested_pu_ids = set(pu_ward_map.keys())

        # map of already-existing pu -> coverage_id
        existing_map = await repo.get_existing_by_pu_ids(project_id, requested_pu_ids)

        # Determine which pus are new
        new_pu_ids = requested_pu_ids - set(existing_map.keys())

        records = []
        for pu_id in new_pu_ids:
            ward_id = pu_ward_map.get(pu_id)
            if not ward_id:
                # no parent ward found — skip or log; we don't want a FK violation
                continue

            ward_cov_id = ward_coverage_map.get(ward_id)
            if not ward_cov_id:
                # no parent coverage found — skip or log; we don't want a FK violation
                continue
            records.append(
                ProjectPuCoverage(
                    project_id=project_id,
                    pu_id=pu_id,
                    ward_coverage_id=ward_cov_id
                )
            )

        if records:
            # repo.bulk_create should insert all records (and commit if your UoW does)
            await repo.bulk_create(records)

        # query again for a complete mapping (existing + newly created)
        full_map = await repo.get_existing_by_pu_ids(project_id, requested_pu_ids)
        return full_map, len(records)

    async def get_state_coverage(self, project_id: str) -> list[ProjectStateCoverage]:
        async with self.uow_factory as uow:
            return await uow.state_coverage_repo.get_state_coverage(project_id)

    async def get_lga_coverage_by_state_id(self, project_id: str, state_coverage_id: str) -> list[ProjectLgaCoverage]:
        async with self.uow_factory as uow:
            return await uow.lga_coverage_repo.get_lga_coverage(project_id=project_id, state_coverage_id=state_coverage_id)

    async def get_ward_coverage_by_lga_id(self, project_id: str, lga_coverage_id: str) -> list[ProjectWardCoverage]:
        async with self.uow_factory as uow:
            return await uow.ward_coverage_repo.get_ward_coverage(project_id=project_id, lga_coverage_id=lga_coverage_id)

    async def get_pu_coverage_by_ward_id(self, project_id: str, ward_coverage_id: str, assigned_status: bool | None = None) -> list[ProjectPuCoverage]:
        async with self.uow_factory as uow:
            return await uow.pu_coverage_repo.get_pu_coverage(project_id=project_id, ward_coverage_id=ward_coverage_id, assigned_status=assigned_status)
