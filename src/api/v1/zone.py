from typing import List, Optional
from uuid import UUID
from http import HTTPStatus

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from src.core.modules import Page
from src.db.postgresql import get_postgresql
from src.schemas.zone import (
    Zone,
    ZoneCreate,
    ZoneUpdate,
)
from src.services.crud.zone import ZoneService, get_zone_service


# Объект router, в котором регистрируем обработчики
router = APIRouter()


@router.get("/{zone_id}", response_model=Zone)
async def get_order(
    *,
    zone_id: UUID,
    db: Session = Depends(get_postgresql),
    service: ZoneService = Depends(get_zone_service),
) -> Optional[Zone]:
    """Get Order by ID

    Args:  
        zone_id (UUID): order ID  

    Returns:  
        Optional[Zone]: Order full data
    """   
    zone = await service.get(db=db, item_id=zone_id)
    if not zone:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Order not found')

    return zone     


@router.get("/", response_model=List[Zone])
async def list_orders(
    *,
    page: Page = Depends(),
    db: Session = Depends(get_postgresql),
    service: ZoneService = Depends(get_zone_service),
) -> Optional[List[Zone]]:
    """Get Orders list

    Args:  
        page (Page, optional): page size and page limits  

    Returns:  
        Optional[List[Order]]: List of Orders
    """
    zones = await service.list(db, skip=page.number, limit=page.size)
    if not zones:
        return []

    return zones      # type: ignore


@router.post("/", response_model=Zone)
async def create_order(
    *,
    zone_in: ZoneCreate,
    db: Session = Depends(get_postgresql),
    service: ZoneService = Depends(get_zone_service),
) -> Zone:
    """Create a new Order

    Args:
        zone_in (ZoneCreate): body request

    Returns:
        Zone: Order full data
    """

    return await service.create(db, obj_in=zone_in)


@router.put("/{zone_id}", response_model=Zone)
async def update_order(
    *,
    zone_id: UUID,
    zone_in: ZoneUpdate,
    db: Session = Depends(get_postgresql),
    service: ZoneService = Depends(get_zone_service),
) -> Optional[Zone]:
    """Update Order

    Args:
        zone_id (UUID): Order ID  

    Returns:
        Optional[Zone]: Order full data
    """
    zone = await service.get(db, item_id=zone_id)
    if not zone:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Order not found')

    return await service.update(db, db_obj=zone, obj_in=zone_in)


@router.delete("/{zone_id}", response_model=Zone)
async def delete_Order(
    *,
    zone_id: UUID,
    db: Session = Depends(get_postgresql),
    service: ZoneService = Depends(get_zone_service),
) -> Zone:
    """Delete a Order

    Args:
        zone_id (UUID): Order ID  

    Returns:
        Zone: Order full data
    """
    zone = await service.get(db, item_id=zone_id)
    if not zone:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Order not found')

    return await service.remove(db, item_id=zone_id)
