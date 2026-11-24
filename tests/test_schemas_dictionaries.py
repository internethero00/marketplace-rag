import uuid
from datetime import UTC, datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from marketplace_rag.models import GemColor, GemType
from marketplace_rag.schemas.gem_type import GemTypeCreate, GemTypeRead, GemTypeUpdate
from marketplace_rag.schemas.shape import ShapeUpdate


def test_gem_type_create_strips_and_dedupes_attributes() -> None:
    schema = GemTypeCreate(
        name="  Ruby ",
        mohs_hardness=Decimal("9"),
        colors=["Red", " red", "Pink"],
        treatments=["Heated", "heated "],
    )

    assert schema.name == "Ruby"
    assert schema.colors == ["Red", "Pink"]
    assert schema.treatments == ["Heated"]


@pytest.mark.parametrize("hardness", ["0.9", "10.1", "7.55"])
def test_gem_type_create_rejects_invalid_hardness(hardness: str) -> None:
    with pytest.raises(ValidationError):
        GemTypeCreate(name="Ruby", mohs_hardness=Decimal(hardness))


def test_create_rejects_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        GemTypeCreate.model_validate({"name": "Ruby", "price": 100})


def test_update_rejects_explicit_null_for_required_fields() -> None:
    with pytest.raises(ValidationError):
        GemTypeUpdate.model_validate({"name": None})
    with pytest.raises(ValidationError):
        ShapeUpdate.model_validate({"is_active": None})


def test_update_allows_null_for_nullable_fields_and_tracks_unset() -> None:
    schema = ShapeUpdate.model_validate({"icon_url": None})

    assert schema.model_dump(exclude_unset=True) == {"icon_url": None}


def test_gem_type_read_from_orm() -> None:
    now = datetime.now(UTC)
    gem_type = GemType(
        id=uuid.uuid4(),
        name="Ruby",
        mohs_hardness=Decimal("9.0"),
        is_active=True,
        created_at=now,
        updated_at=now,
    )
    gem_type.colors = [GemColor(id=uuid.uuid4(), name="Red")]

    schema = GemTypeRead.model_validate(gem_type)

    assert schema.colors[0].name == "Red"
    assert schema.treatments == []
