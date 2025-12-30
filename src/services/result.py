from src.unit_of_work.unit_of_work import UnitOfWork
from src.schemas.result import SubmitResultSchema
from src.models.enums import ElectionRole, ResultStatus
from src.models.result import Result
from src.models.media import ResultMedia
from src.models.party_vote import PartyVote
from src.validations.result import (validate_pu_exists, validate_authorized_user,
                                    validate_result_not_exists, validate_pu_coverage
                                    )


class ResultService:
    """Service for handling results related operations"""

    def __init__(self, uow_factory: UnitOfWork) -> None:
        self.uow_factory = uow_factory

    async def submit_result(
        self,
        project_id: str,
        user_id: str,
        result_data: SubmitResultSchema
    ) -> Result:
        """Submit election result for a polling unit"""
        async with self.uow_factory as uow:
            # validate_pu_exists
            await validate_pu_exists(
                uow=uow,
                pu_id=result_data.pu_id
            )
            # validate_pu_covered
            await validate_pu_coverage(
                uow=uow.pu_coverage_repo,
                project_id=project_id,
                pu_id=result_data.pu_id
            )

            # validate that the user is authorized to submit results for the project
            await validate_authorized_user(
                uow=uow,
                user_id=user_id,
                project_id=project_id,
                pu_id=result_data.pu_id
            )

            # validate_result_not_exists
            await validate_result_not_exists(
                uow=uow.result_repo,
                project_id=project_id,
                pu_id=result_data.pu_id
            )

            # Validte data passed business rules
            # (e.g., total votes consistency, accredited voters limits, etc.)
            # This can be implemented as needed.

            # Create Result entity
            result_entity = Result(
                project_id=project_id,
                polling_unit_id=result_data.pu_id,
                submitted_by_user_id=user_id,
                accredited_voters=result_data.accredited_voters,
                total_votes_cast=result_data.total_votes_cast,
                total_valid_votes=result_data.total_valid_votes,
                total_invalid_votes=result_data.total_invalid_votes,
                total_cancelled_votes=result_data.total_cancelled_votes,
                remarks=result_data.remarks,
                status=ResultStatus.PENDING_REVIEW
            )

            # Add media files if any
            for media in result_data.media:
                media_entity = ResultMedia(
                    result_id=result_entity.id,
                    media_url=media.media_url,
                    media_type=media.media_type
                )
                result_entity.media_files.append(media_entity)

            # Add party votes
            for party_vote in result_data.party_votes:
                party_vote_entity = PartyVote(
                    result_id=result_entity.id,
                    party_id=party_vote.party_id,
                    votes=party_vote.valid_votes
                )
                result_entity.party_votes.append(party_vote_entity)

            # Save the result
            result = await uow.result_repo.create(result_entity)
            return result
