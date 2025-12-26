from uuid import uuid4
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import String, DateTime
from datetime import datetime, timezone



class Base(DeclarativeBase):
    pass
    

class Basemodel:
    id: Mapped[str] = mapped_column(String(60), nullable=False, primary_key=True, default=lambda: str(uuid4()))
    full_name: Mapped [str] = mapped_column()
    email: Mapped[str] = mapped_column(String(60), nullable=False)
    created_at: Mapped[str] = mapped_column(DateTime(timezone), default=datetime.now(timezone.utc))
    updated_at: Mapped[str] = mapped_column(DateTime(timezone), default=datetime.now(timezone.utc))
    
