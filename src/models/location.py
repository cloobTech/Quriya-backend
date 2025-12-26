from sqlalchemy.orm import mapped_column, Mapped
from models.base import Basemodel, Base

class Location(Basemodel, Base):
    __tablename__ = "locations"

    city: Mapped[str] = mapped_column()
    state: Mapped[str] = mapped_column()

    