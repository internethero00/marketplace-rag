import uuid
from datetime import datetime
from typing import Annotated

from pydantic import StringConstraints, field_validator

from marketplace_rag.schemas.common import InputSchema, ReadSchema, ensure_not_null

ShapeName = Annotated[str, StringConstraints(min_length=1, max_length=100)]

IconUrl = Annotated[str, StringConstraints(min_length=1, max_length=500)]


class ShapeCreate(InputSchema):
    name: ShapeName
    icon_url: IconUrl | None = None
    is_active: bool = True


class ShapeUpdate(InputSchema):
    name: ShapeName | None = None
    icon_url: IconUrl | None = None
    is_active: bool | None = None

    @field_validator("name", "is_active")
    @classmethod
    def forbid_null(cls, value: object) -> object:
        return ensure_not_null(value)


class ShapeRead(ReadSchema):
    id: uuid.UUID
    name: str
    icon_url: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime
