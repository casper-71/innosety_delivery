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
from src.schemas.delivery import (
    Delivery,
    DeliveryCreate,
    DeliveryUpdate,
)
from src.services.crud.delivery import DeliveryService, get_delivery_service


# Объект router, в котором регистрируем обработчики
router = APIRouter()


@router.get("/{delivery_id}", response_model=Delivery)
async def get_delivery(
    *,
    delivery_id: UUID,
    db: Session = Depends(get_postgresql),
    service: DeliveryService = Depends(get_delivery_service),
) -> Optional[Delivery]:
    """Get delivery by ID

    Args:  
        delivery_id (UUID): delivery ID  

    Returns:  
        Optional[Delivery]: delivery full data
    """   
    delivery = await service.get(db=db, item_id=delivery_id)
    if not delivery:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='delivery not found')

    return delivery     


@router.get("/", response_model=List[Delivery])
async def list_deliveries(
    *,
    page: Page = Depends(),
    db: Session = Depends(get_postgresql),
    service: DeliveryService = Depends(get_delivery_service),
) -> Optional[List[Delivery]]:
    """Get deliveries list

    Args:  
        page (Page, optional): page size and page limits  

    Returns:  
        Optional[List[Delivery]]: List of Deliverys
    """
    Deliverys = await service.list(db, skip=page.number, limit=page.size)
    if not Deliverys:
        return []

    return Deliverys      # type: ignore


@router.post("/", response_model=Delivery)
async def create_delivery(
    *,
    delivery_in: DeliveryCreate,
    db: Session = Depends(get_postgresql),
    service: DeliveryService = Depends(get_delivery_service),
) -> Delivery:
    """Create a new Delivery

    Args:
        delivery_in (DeliveryCreate): body request

    Returns:
        Delivery: Delivery full data
    """

    return await service.create(db, obj_in=delivery_in)


@router.put("/{delivery_id}", response_model=Delivery)
async def update_delivery(
    *,
    delivery_id: UUID,
    delivery_in: DeliveryUpdate,
    db: Session = Depends(get_postgresql),
    service: DeliveryService = Depends(get_delivery_service),
) -> Optional[Delivery]:
    """Update Delivery

    Args:
        delivery_id (UUID): Delivery ID  

    Returns:
        Optional[Delivery]: Delivery full data
    """
    delivery = await service.get(db, item_id=delivery_id)
    if not delivery:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Delivery not found')

    return await service.update(db, db_obj=delivery, obj_in=delivery_in)


@router.delete("/{delivery_id}", response_model=Delivery)
async def delete_Delivery(
    *,
    delivery_id: UUID,
    db: Session = Depends(get_postgresql),
    service: DeliveryService = Depends(get_delivery_service),
) -> Delivery:
    """Delete a Delivery

    Args:
        delivery_id (UUID): Delivery ID  

    Returns:
        Delivery: Delivery full data
    """
    delivery = await service.get(db, item_id=delivery_id)
    if not delivery:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='delivery not found')

    return await service.remove(db, item_id=delivery_id)
