from src.unit_of_work.unit_of_work import UnitOfWork
from src.schemas.project_coverage import CoverageSelection
from src.models.project_state_coverage import ProjectStateCoverage
from src.models.project_lga_coverage import ProjectLgaCoverage
from src.models.project_ward_coverage import ProjectWardCoverage
from src.models.project_pu_coverage import ProjectPuCoverage
from src.validations.coverage import validate_project_exists, validate_coverage_selection, validate_location_existence


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
            stats["states"] = await self.bulk_create_coverage(repo=uow.state_coverage_repo, project_id=project_id, ids=validated_state_ids, model_cls=ProjectStateCoverage, field_name="state_id")

            # LGA
            validated_lga_ids = await validate_location_existence(repo=uow.lga_repo, ids=data.lga_ids)
            stats["lgas"] = await self.bulk_create_coverage(repo=uow.lga_coverage_repo, project_id=project_id, ids=validated_lga_ids, model_cls=ProjectLgaCoverage, field_name="lga_id")

            # Ward
            validated_ward_ids = await validate_location_existence(repo=uow.ward_repo, ids=data.ward_ids)
            stats["wards"] = await self.bulk_create_coverage(repo=uow.ward_coverage_repo, project_id=project_id, ids=validated_ward_ids, model_cls=ProjectWardCoverage, field_name="ward_id")

            # PUs
            validated_pu_ids = await validate_location_existence(repo=uow.polling_unit_repo, ids=data.polling_unit_ids)
            stats["pus"] = await self.bulk_create_coverage(repo=uow.pu_coverage_repo, project_id=project_id, ids=validated_pu_ids, model_cls=ProjectPuCoverage, field_name="pu_id")

            stats["total"] = sum(stats.values())

            return {
                "message": "Coverages created successfully",
                "stats": stats
            }

    async def bulk_create_coverage(
        self,
        repo,
        project_id: str,
        ids: set[str],
        model_cls: type,
        field_name: str,
        batch_size: int = 1000
    ):
        if not ids:
            return

        # Add only Locations not already under project coverage
        existing_ids = await repo.get_existing_ids(project_id, ids, field_name)
        new_ids = ids - existing_ids

        records = [
            model_cls(project_id=project_id, **{field_name: _id})
            for _id in new_ids
        ]
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            await repo.bulk_create(batch)
        return len(records)
