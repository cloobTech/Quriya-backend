from src.events.base import DomainEvent


class UserCreatedEvent(DomainEvent):
    email: str
    first_name: str
    last_name: str

