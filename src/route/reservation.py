import uuid as uuid

from fastapi import APIRouter
from pydantic import BaseModel
from .storage import OrderType, InMemoryStorage, GetAllFilter
from datetime import *

router = APIRouter(prefix="/reservation")

class Reservation(BaseModel):
    date_debut: date
    date_fin: date
    chambre_id: int
    token: str
    checkint:int

@router.get("/")
def get_allReservation(order:str=None, order_type:OrderType = OrderType.DESC, limit:int=None, offset:int=None) -> list[Reservation]:
    filter = GetAllFilter()
    filter.order = order
    filter.order_type = order_type
    filter.limit = limit
    filter.offset = offset
    rs = InMemoryStorage.for_type(Reservation).get_all(filter)
    return rs

@router.get("/{uuid}")
def get_uneReservation(uuid:uuid.UUID) -> Reservation:
    rs = InMemoryStorage.for_type(Reservation).get(uuid)
    if not rs:
        raise ValueError()
    return rs

@router.post("/")
def add_reservation(resrvation: Reservation) -> uuid.UUID:
    new_uuid = InMemoryStorage.for_type(Reservation).create(resrvation)
    return new_uuid

@router.delete("/{id}")
def delete_reservation(id: uuid.UUID):
    success = InMemoryStorage.for_type(Reservation).delete(id)
    if not success:
        raise ValueError(f"Reservation with id {id} not found.")
    return {"message": "Reservation deleted successfully"}
    

@router.patch("/{uid}")
def edit_reservation(uid: uuid.UUID, item: Reservation) -> bool:
    rs = InMemoryStorage.for_type(Reservation).get(uid)
    if not rs:
        return False
    update_data = item.dict(exclude_unset=True)
    InMemoryStorage.for_type(Reservation).update(uid, rs.copy(update=update_data))
    return True