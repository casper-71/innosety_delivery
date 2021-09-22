import orjson

from datetime import datetime
from typing import Optional, Any
from uuid import UUID
from pydantic import (
    BaseModel,
    Field,
)

from src.models.order import OrderStatus
from src.schemas.delivery import Delivery
from src.schemas.zone import Zone


def orjson_dumps(v, *, default):
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    # https://pydantic-docs.helpmanual.io/usage/exporting_models/#custom-json-deserialisation
    return orjson.dumps(v, default=default).decode()    # pylint: disable=no-member


# Shared properties
class OrderBase(BaseModel):
    status: OrderStatus = Field(
        default=OrderStatus.NOT_DELIVERED,
        description='''Order создается в статусе `not_delivered`''',
    )

    class Config:
        json_loads = orjson.loads       # pylint: disable=no-member
        json_dumps = orjson_dumps
        allow_population_by_field_name = True


# Properties to receive on Order creation
class OrderCreate(OrderBase):
    customer_id: UUID
    courier_id: UUID
    delivery_date: datetime

    desctiption: Optional[str]

    created_by: str
    updated_by: Optional[str] 

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.updated_by = self.created_by


class OrderUpdate(OrderBase):
    courier_id: Optional[UUID]
    delivery_date: Optional[datetime]
    desctiption: Optional[str]

    updated_by: str


class OrderInDBBase(OrderBase):
    id: Optional[UUID]
    customer_id: Optional[UUID]
    courier_id: Optional[UUID]

    delivery_date: Optional[datetime]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


class Order(OrderInDBBase):
    pass


class OrderFull(OrderInDBBase):
    updated_at: Optional[datetime]
    description: Optional[str]
    delivery: Delivery
    zone: Zone
