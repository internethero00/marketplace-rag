from pydantic import BaseModel, ConfigDict


class InputSchema(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class ReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


def ensure_not_null[T](value: T | None) -> T:
    if value is None:
        raise ValueError("field cannot be null")
    return value


def remove_duplicate_names(names: list[str]) -> list[str]:
    seen_names: set[str] = set()
    unique_names: list[str] = []

    for name in names:
        normalized_name = name.casefold()
        if normalized_name in seen_names:
            continue
        seen_names.add(normalized_name)
        unique_names.append(name)

    return unique_names
