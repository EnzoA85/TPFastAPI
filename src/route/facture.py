import uuid as uuid

from fastapi import APIRouter
from pydantic import BaseModel
from .storage import OrderType, InMemoryStorage, GetAllFilter

router = APIRouter(prefix="/facture")

class Facture(BaseModel):
    client_id: int
    num: int

@router.get("/")
def get_allFacture(order:str=None, order_type:OrderType = OrderType.DESC, limit:int=None, offset:int=None) -> list[Facture]:
    filter = GetAllFilter()
    filter.order = order
    filter.order_type = order_type
    filter.limit = limit
    filter.offset = offset
    fc = InMemoryStorage.for_type(Facture).get_all(filter)
    return fc

@router.get("/{uuid}")
def get_uneFacture(uuid:uuid.UUID) -> Facture:
    fc = InMemoryStorage.for_type(Facture).get(uuid)
    if not fc:
        raise ValueError()
    return fc