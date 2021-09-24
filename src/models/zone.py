from sqlalchemy import (
    Column,
    String,
    Float,
)

from src.db.postgresql import Base
from src.models.base_mixins import BaseMixin, TimestampMixin


class Zone(Base, BaseMixin, TimestampMixin):
    """ Модель зоны доставки """

    name = Column(String, nullable=False)
    coordinates = Column(ARRAY(Float), nullable=False)

    def __repr__(self) -> str:
        return f"<Zone {self.id}>"
