from models.base import Basemodel, Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from typing import Optional

class admin(Basemodel, Base):
    __tablename__ = "admins"

    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    password: Mapped[str] = mapped_column(nullable=False)
    