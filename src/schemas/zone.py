import orjson

from datetime import datetime
from typing import Optional, Any
from uuid import UUID
from pydantic import (
    BaseModel,
)


def orjson_dumps(v, *, default):
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    # https://pydantic-docs.helpmanual.io/usage/exporting_models/#custom-json-deserialisation
    return orjson.dumps(v, default=default).decode()    # pylint: disable=no-member


class ZoneBase(BaseModel):

    class Config:
        json_loads = orjson.loads       # pylint: disable=no-member
        json_dumps = orjson_dumps
        allow_population_by_field_name = True


# Properties to receive on Zone creation
class ZoneCreate(ZoneBase):
    name: str
    longitude: float
    latitude: float

    created_by: str
    updated_by: Optional[str] 

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.updated_by = self.created_by


class ZoneUpdate(ZoneBase):
    name: Optional[str]
    longitude: Optional[float]
    latitude: Optional[float]

    updated_by: str


class ZoneInDBBase(ZoneBase):
    id: Optional[UUID]
    name: Optional[str]
    longitude: Optional[float]
    latitude: Optional[float]

    created_at: Optional[datetime]
    created_by: Optional[str]
    updated_by: Optional[str]

    class Config:
        orm_mode = True


class Zone(ZoneInDBBase):
    pass
