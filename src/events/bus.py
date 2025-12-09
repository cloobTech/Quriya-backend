import asyncio
import inspect
from typing import Type, Dict, List, Callable, Awaitable, Union, Any, TypeVar, Generic
from src.events.base import DomainEvent

E = TypeVar("E", bound=DomainEvent)

Handler = Union[
    Callable[[E], Awaitable[Any]],   # async handler
    Callable[[E], Any]               # sync handler
]


class EventBus(Generic[E]):
    def __init__(self):
        self._subscribers: Dict[Type[E], List[Handler]] = {}

    def subscribe(self, event_type: Type[E], handler: Handler):
        self._subscribers.setdefault(event_type, []).append(handler)

    async def publish(self, event: E):
        handlers = self._subscribers.get(type(event), [])
        tasks = []

        for handler in handlers:
            if inspect.iscoroutinefunction(handler):
                tasks.append(asyncio.create_task(handler(event)))
            else:
                loop = asyncio.get_running_loop()
                tasks.append(loop.run_in_executor(None, handler, event))

        await asyncio.gather(*tasks, return_exceptions=True)


event_bus = EventBus()
