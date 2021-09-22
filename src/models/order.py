import enum

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    DateTime,
    String,
    Enum,
)

from src.db.postgresql import Base
from src.models.base_mixins import BaseMixin, TimestampMixin, AuditMixin
from src.models.history_meta import Versioned

# Этот импорт нужен для связи one-to-one для модели Order
from src.models.delivery import Delivery            # noqa: F401
from src.models.zone import Zone                    # noqa: F401


class OrderStatus(enum.Enum):
    """ Статусы доставки:
        принял заказ, осуществляю доставку, доставил, не доставил
    """    
    ACCEPT = 'accept'
    DELIVERING = 'delivering'
    DELIVERED = 'delivered'
    NOT_DELIVERED = 'not_delivered'


class OrderMixin(TimestampMixin, AuditMixin):
    """ Order base model """

    customer_id = Column(UUID(as_uuid=True), nullable=False)
    courier_id = Column(UUID(as_uuid=True), nullable=False)
    delivery_date = Column(DateTime, nullable=False)
    desctiption = Column(String, nullable=True)
    status = Column(Enum(OrderStatus, nullable=False, default=OrderStatus.NOT_DELIVERED))


class Order(Versioned, Base, BaseMixin, OrderMixin):
    """[summary]

    Args:
        Versioned ([type]): [description]
        Base ([type]): [description]
        BaseMixin ([type]): [description]
        OrderMixin ([type]): [description]
    """    
    @declared_attr
    def delivery(cls):              # pylint: disable=no-self-argument
        return relationship(
            "Delivery",
            backref="order",
            cascade="all, delete",
            uselist=False,
        )

    @declared_attr
    def zone(cls):                  # pylint: disable=no-self-argument
        return relationship(
            "Zone",
            backref="order",
            cascade="all, delete",
            uselist=False,
        )

    def __repr__(self) -> str:
        return f"<Order {self.id}>"
