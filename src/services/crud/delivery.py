from src.models.history_meta import versioned_session
from uuid import UUID
from functools import lru_cache
from sqlalchemy.orm import Session
from typing import (
    Optional,
    List,
    Union,
    Dict,
    Any,
)

from src.schemas import delivery as delivery_schema
from src.models import delivery as delivery_model
from src.services.crud.base import CRUDBase


class DeliveryService(
    CRUDBase[delivery_model.Delivery, delivery_schema.DeliveryCreate, delivery_schema.DeliveryUpdate]
):

    async def get(self, db: Session, item_id: UUID) -> Optional[delivery_model.Delivery]:
        """ Get Delivery by ID

        Args:
            db (Session): SQLAlchemy Session
            item_id (UUID): Delivery ID

        Returns:
            Optional[delivery_model.Delivery]: Delivery full data
        """

        return await super().get(db, item_id)

    async def list(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[delivery_model.Delivery]:
        """ List of Deliverys

        Args:
            db (Session): SQLAlchemy Session
            skip (int): page number
            limit (int): page limit

        Returns:
            List[delivery_model.Delivery]: List of Deliverys
        """        """  """
        return await super().list(db, skip=skip, limit=limit)

    async def create(self, db: Session, *, obj_in: delivery_schema.DeliveryCreate) -> delivery_model.Delivery:
        """Create a Delivery

        Args:
            db (Session): SQLAlchemy Session
            obj_in (delivery_schema.DeliveryCreate): request parameters

        Returns:
            delivery_model.Delivery: Delivery full data
        """     
        versioned_session(db)
        return await super().create(db, obj_in=obj_in)

    async def update(
        self, db: Session,
        *,
        db_obj: delivery_model.Delivery,
        obj_in: Union[delivery_schema.DeliveryUpdate, Dict[str, Any]]
    ) -> delivery_model.Delivery:
        """ Update Delivery

        Args:
            db (Session): SQLAlchemy Session
            db_obj (delivery_model.Delivery): Database model of Delivery
            obj_in (Union[delivery_schema.DeliveryUpdate, Dict[str, Any]]): request parameters

        Returns:
            delivery_model.Delivery: Delivery full data
        """
        versioned_session(db)
        return await super().update(db, db_obj=db_obj, obj_in=obj_in)

    async def remove(self, db: Session, *, item_id: UUID) -> delivery_model.Delivery:
        """Delete Delivery

        Args:
            db (Session): SQLAlchemy Session
            item_id (UUID): Delivery ID

        Returns:
            delivery_model.Delivery: Delivery full data
        """        
        return await super().remove(db, item_id=item_id)


@lru_cache
def get_delivery_service() -> DeliveryService:
    return DeliveryService(
        delivery_model.Delivery,
    )
