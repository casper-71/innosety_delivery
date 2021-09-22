from sqlalchemy.sql.schema import ForeignKey

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    Column,
    Float,
)

from src.db.postgresql import Base
from src.models.base_mixins import BaseMixin, TimestampMixin, AuditMixin
from src.models.history_meta import Versioned


class DeliveryMixin(TimestampMixin, AuditMixin):
    """ Delivery base model """

    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), onupdate="CASCADE")
    zone_id = Column(UUID(as_uuid=True), ForeignKey("zones.id"), onupdate="CASCADE")
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)


class Delivery(Versioned, Base, BaseMixin, DeliveryMixin):
    """ Модель хранит информацию о доставке  """    

    def __repr__(self) -> str:
        return f"<Delivery {self.id}>"
