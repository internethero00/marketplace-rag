import uuid
from datetime import datetime
from decimal import Decimal
from typing import Annotated

from pydantic import AfterValidator, Field, StringConstraints, field_validator

from marketplace_rag.schemas.common import (
    InputSchema,
    ReadSchema,
    ensure_not_null,
    remove_duplicate_names,
)

GemTypeName = Annotated[str, StringConstraints(min_length=1, max_length=100)]

AttributeName = Annotated[str, StringConstraints(min_length=1, max_length=50)]

UniqueAttributeNames = Annotated[list[AttributeName], AfterValidator(remove_duplicate_names)]

MohsHardness = Annotated[Decimal, Field(ge=1, le=10, max_digits=3, decimal_places=1)]


class GemAttributeCreate(InputSchema):
    name: AttributeName


class GemAttributeRead(ReadSchema):
    id: uuid.UUID
    name: str


class GemTypeCreate(InputSchema):
    name: GemTypeName
    mohs_hardness: MohsHardness | None = None
    is_active: bool = True
    colors: UniqueAttributeNames = Field(default_factory=list)
    treatments: UniqueAttributeNames = Field(default_factory=list)


class GemTypeUpdate(InputSchema):
    name: GemTypeName | None = None
    mohs_hardness: MohsHardness | None = None
    is_active: bool | None = None

    @field_validator("name", "is_active")
    @classmethod
    def forbid_null(cls, value: object) -> object:
        return ensure_not_null(value)


class GemTypeShort(ReadSchema):
    id: uuid.UUID
    name: str


class GemTypeRead(ReadSchema):
    id: uuid.UUID
    name: str
    mohs_hardness: Decimal | None
    is_active: bool
    colors: list[GemAttributeRead]
    treatments: list[GemAttributeRead]
    created_at: datetime
    updated_at: datetime
