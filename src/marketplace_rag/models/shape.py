from sqlalchemy import String, true
from sqlalchemy.orm import Mapped, mapped_column

from marketplace_rag.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Shape(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "shapes"

    name: Mapped[str] = mapped_column(String(100), unique=True)
    icon_url: Mapped[str | None] = mapped_column(String(500))
    is_active: Mapped[bool] = mapped_column(default=True, server_default=true())
