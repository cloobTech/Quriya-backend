from models.base import Basemodel, Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, ForeignKey
from typing import Optional

class Customer(Basemodel, Base):

    preferred_location: Mapped[str] = mapped_column(String(250), nullable=False)

    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))

    