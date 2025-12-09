from src.events.user_events import UserCreatedEvent
from src.tasks.email_task import dispatch_email


async def handle_user_created(event: UserCreatedEvent):
    assert isinstance(event, UserCreatedEvent)
    user = event

    dispatch_email.delay(
        email_list=[user.email],
        subject="Welcome to Our Service!",
        template_name="test_template.html",
        context={"first_name": user.first_name}
    )
