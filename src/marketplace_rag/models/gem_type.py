import uuid
from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String, UniqueConstraint, true
from sqlalchemy.orm import Mapped, mapped_column, relationship

from marketplace_rag.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class GemType(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "gem_types"
    __table_args__ = (
        CheckConstraint("mohs_hardness BETWEEN 1 AND 10", name="mohs_hardness_range"),
    )

    name: Mapped[str] = mapped_column(String(100), unique=True)
    mohs_hardness: Mapped[Decimal | None] = mapped_column(Numeric(3, 1))
    is_active: Mapped[bool] = mapped_column(default=True, server_default=true())

    colors: Mapped[list["GemColor"]] = relationship(
        back_populates="gem_type",
        cascade="all, delete-orphan",
        order_by="GemColor.name",
        lazy="selectin",
    )
    treatments: Mapped[list["GemTreatment"]] = relationship(
        back_populates="gem_type",
        cascade="all, delete-orphan",
        order_by="GemTreatment.name",
        lazy="selectin",
    )


class GemColor(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "gem_colors"
    __table_args__ = (UniqueConstraint("gem_type_id", "name"),)

    gem_type_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("gem_types.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(50))

    gem_type: Mapped[GemType] = relationship(back_populates="colors")


class GemTreatment(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "gem_treatments"
    __table_args__ = (UniqueConstraint("gem_type_id", "name"),)

    gem_type_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("gem_types.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(50))

    gem_type: Mapped[GemType] = relationship(back_populates="treatments")
