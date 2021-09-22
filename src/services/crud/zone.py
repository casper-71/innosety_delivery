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

from src.schemas import zone as zone_schema
from src.models import zone as zone_model
from src.services.crud.base import CRUDBase


class ZoneService(CRUDBase[zone_model.Zone, zone_schema.ZoneCreate, zone_schema.ZoneUpdate]):

    async def get(self, db: Session, item_id: UUID) -> Optional[zone_model.Zone]:
        """ Get Zone by ID

        Args:
            db (Session): SQLAlchemy Session
            item_id (UUID): Zone ID

        Returns:
            Optional[zone_model.Zone]: Zone full data
        """

        return await super().get(db, item_id)

    async def list(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[zone_model.Zone]:
        """ List of Zones

        Args:
            db (Session): SQLAlchemy Session
            skip (int): page number
            limit (int): page limit

        Returns:
            List[zone_model.Zone]: List of Zones
        """        """  """
        return await super().list(db, skip=skip, limit=limit)

    async def create(self, db: Session, *, obj_in: zone_schema.ZoneCreate) -> zone_model.Zone:
        """Create a Zone

        Args:
            db (Session): SQLAlchemy Session
            obj_in (zone_schema.ZoneCreate): request parameters

        Returns:
            zone_model.Zone: Zone full data
        """     
        versioned_session(db)
        return await super().create(db, obj_in=obj_in)

    async def update(
        self, db: Session, *, db_obj: zone_model.Zone, obj_in: Union[zone_schema.ZoneUpdate, Dict[str, Any]]
    ) -> zone_model.Zone:
        """ Update Zone

        Args:
            db (Session): SQLAlchemy Session
            db_obj (zone_model.Zone): Database model of Zone
            obj_in (Union[zone_schema.ZoneUpdate, Dict[str, Any]]): request parameters

        Returns:
            zone_model.Zone: Zone full data
        """
        versioned_session(db)
        return await super().update(db, db_obj=db_obj, obj_in=obj_in)

    async def remove(self, db: Session, *, item_id: UUID) -> zone_model.Zone:
        """Delete Zone

        Args:
            db (Session): SQLAlchemy Session
            item_id (UUID): Zone ID

        Returns:
            zone_model.Zone: Zone full data
        """        
        return await super().remove(db, item_id=item_id)


@lru_cache
def get_zone_service() -> ZoneService:
    return ZoneService(
        zone_model.Zone,
    )
