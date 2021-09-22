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
from src.schemas.order import (
    Order,
    OrderFull,
    OrderCreate,
    OrderUpdate,
)
from src.services.crud.order import orderService, get_order_service


# Объект router, в котором регистрируем обработчики
router = APIRouter()


@router.get("/{order_id}", response_model=OrderFull)
async def get_order(
    *,
    order_id: UUID,
    db: Session = Depends(get_postgresql),
    service: orderService = Depends(get_order_service),
) -> Optional[OrderFull]:
    """Get Order by ID

    Args:  
        order_id (UUID): order ID  

    Returns:  
        Optional[OrderFull]: Order full data
    """   
    order = await service.get(db=db, item_id=order_id)
    if not order:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Order not found')

    return order     


@router.get("/", response_model=List[Order])
async def list_orders(
    *,
    page: Page = Depends(),
    db: Session = Depends(get_postgresql),
    service: orderService = Depends(get_order_service),
) -> Optional[List[Order]]:
    """Get Orders list

    Args:  
        page (Page, optional): page size and page limits  

    Returns:  
        Optional[List[Order]]: List of Orders
    """
    orders = await service.list(db, skip=page.number, limit=page.size)
    if not orders:
        return []

    return orders      # type: ignore


@router.post("/", response_model=OrderFull)
async def create_order(
    *,
    order_in: OrderCreate,
    db: Session = Depends(get_postgresql),
    service: orderService = Depends(get_order_service),
) -> OrderFull:
    """Create a new Order

    Args:
        Order_in (OrderCreate): body request

    Returns:
        OrderFull: Order full data
    """

    return await service.create(db, obj_in=order_in)


@router.put("/{order_id}", response_model=OrderFull)
async def update_order(
    *,
    order_id: UUID,
    order_in: OrderUpdate,
    db: Session = Depends(get_postgresql),
    service: orderService = Depends(get_order_service),
) -> Optional[OrderFull]:
    """Update Order

    Args:
        order_id (UUID): Order ID  

    Returns:
        Optional[OrderFull]: Order full data
    """
    order = await service.get(db, item_id=order_id)
    if not order:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Order not found')

    return await service.update(db, db_obj=order, obj_in=order_in)


@router.delete("/{order_id}", response_model=OrderFull)
async def delete_Order(
    *,
    order_id: UUID,
    db: Session = Depends(get_postgresql),
    service: orderService = Depends(get_order_service),
) -> OrderFull:
    """Delete a Order

    Args:
        order_id (UUID): Order ID  

    Returns:
        OrderFull: Order full data
    """
    order = await service.get(db, item_id=order_id)
    if not order:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Order not found')

    return await service.remove(db, item_id=order_id)
