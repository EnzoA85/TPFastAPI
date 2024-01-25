import enum
import uuid as uuid

from fastapi import APIRouter
from pydantic import BaseModel
from .storage import OrderType, InMemoryStorage, GetAllFilter

router = APIRouter(prefix="/chambre")

class TypeRoom(enum.StrEnum):
    SIMPLE = enum.auto()
    DOUBLE = enum.auto()

class Chambre(BaseModel):
    number: int
    price: float
    type_room: TypeRoom

class ChambreFull(Chambre):
    id: uuid.UUID

@router.get("/{uuid}")
def get_uneChambre(uuid:uuid.UUID) -> Chambre:
    ch = InMemoryStorage.for_type(Chambre).get(uuid)
    if not ch:
        raise ValueError()
    return ch

@router.get("/")
def get_allChambre(order:str=None, order_type:OrderType = OrderType.DESC, limit:int=None, offset:int=None) -> list[Chambre]:
    filter = GetAllFilter()
    filter.order = order
    filter.order_type = order_type
    filter.limit = limit
    filter.offset = offset
    chs = InMemoryStorage.for_type(Chambre).get_all(filter)
    return chs

@router.patch("/{uid}")
def edit_chambre(uid: uuid.UUID, item: Chambre) -> bool:
    ch = InMemoryStorage.for_type(Chambre).get(uid)
    if not ch:
        return False
    update_data = item.dict(exclude_unset=True)
    InMemoryStorage.for_type(Chambre).update(uid, ch.copy(update=update_data))
    return True

@router.post("/")
def add_chambre(chambre: Chambre) -> uuid.UUID:
    new_uuid = InMemoryStorage.for_type(Chambre).create(chambre)
    return new_uuid
