from src.events.handlers.user_handler import handle_user_created
from src.events.handlers.organization_handler import handle_organization_created
from src.events.organization_events import OrganizationCreatedEvent
from src.events.user_events import UserCreatedEvent
from src.events.bus import event_bus


def bootstrap_events_initializer():
    event_bus.subscribe(UserCreatedEvent, handle_user_created)
    event_bus.subscribe(OrganizationCreatedEvent, handle_organization_created)
