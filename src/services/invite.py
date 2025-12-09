from src.services.organization import OrganizationService
from src.services.user import UserService


# send_invite(email, org_id, role)

# verify_invite(token)

# accept_invite(token)

# expire_invite(token)

class InvitationService:
    """Handles sending and accepting invites"""
    def __init__(self, org_service: OrganizationService, user_service: UserService) -> None:
        self.org_service = org_service
        self.user_service = user_service



    async def send_activation_invite(self, org_id:str, user_id: str):
        pass