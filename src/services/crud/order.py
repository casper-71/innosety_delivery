from src.models.history_meta import versioned_session
from uuid import UUID
from functools import lru_cache
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import (
    Optional,
    List,
    Union,
    Dict,
    Any,
)

from src.schemas import order as order_schema
from src.models import order as order_model
from src.services.crud.base import CRUDBase


class orderService(CRUDBase[order_model.Order, order_schema.OrderCreate, order_schema.OrderUpdate]):

    async def get(self, db: Session, item_id: UUID) -> Optional[order_model.Order]:
        """ Get order by ID

        Args:
            db (Session): SQLAlchemy Session
            item_id (UUID): order ID

        Returns:
            Optional[order_model.Order]: order full data
        """

        return await super().get(db, item_id)

    async def list(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[order_model.Order]:
        """ List of orders

        Args:
            db (Session): SQLAlchemy Session
            skip (int): page number
            limit (int): page limit

        Returns:
            List[order_model.Order]: List of orders
        """        """  """
        return await super().list(db, skip=skip, limit=limit)

    async def create(self, db: Session, *, obj_in: order_schema.OrderCreate) -> order_model.Order:
        """Create a order

        Args:
            db (Session): SQLAlchemy Session
            obj_in (order_schema.orderCreate): request parameters

        Returns:
            order_model.order: order full data
        """     
        versioned_session(db)
        data_in_obj = jsonable_encoder(obj_in)
        db_obj = order_model.Order(**data_in_obj)
        db_obj.status = obj_in.status

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    async def update(
        self, db: Session, *, db_obj: order_model.Order, obj_in: Union[order_schema.OrderUpdate, Dict[str, Any]]
    ) -> order_model.Order:
        """ Update order

        Args:
            db (Session): SQLAlchemy Session
            db_obj (order_model.Order): Database model of order
            obj_in (Union[order_schema.OrderUpdate, Dict[str, Any]]): request parameters

        Returns:
            order_model.Order: order full data
        """
        versioned_session(db)
        return await super().update(db, db_obj=db_obj, obj_in=obj_in)

    async def remove(self, db: Session, *, item_id: UUID) -> order_model.Order:
        """Delete order

        Args:
            db (Session): SQLAlchemy Session
            item_id (UUID): order ID

        Returns:
            order_model.Order: order full data
        """        
        return await super().remove(db, item_id=item_id)


@lru_cache
def get_order_service() -> orderService:
    return orderService(
        order_model.Order,
    )
