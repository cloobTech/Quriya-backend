from src.events.organization_events import OrganizationCreatedEvent
from src.tasks.email_task import dispatch_email


async def handle_organization_created(event: OrganizationCreatedEvent):
    assert isinstance(event, OrganizationCreatedEvent)
    organization = event

    dispatch_email.delay(
        email_list=[organization.admin_email],
        subject="Welcome to Our Organization Platform!",
        template_name="organization_created.html",
        context={"organization_name": organization.organization_name,
                 "year": organization.year, "admin_name": organization.admin_name}
    )
