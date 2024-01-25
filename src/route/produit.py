import enum
import uuid as uuid

from fastapi import APIRouter
from pydantic import BaseModel
from .storage import OrderType, InMemoryStorage, GetAllFilter

router = APIRouter(prefix="/produit")

class TypeProduit(enum.StrEnum):
    ALIMENTAIRE = enum.auto()
    BOISSON = enum.auto()
    COSMETIQUE = enum.auto()

class Produit(BaseModel):
    prix_unitaire: int
    nom: str
    type_produit: TypeProduit

@router.get("/{uuid}")
def get_uneProduit(uuid:uuid.UUID) -> Produit:
    pr = InMemoryStorage.for_type(Produit).get(uuid)
    if not pr:
        raise ValueError()
    return pr


@router.get("/")
def get_allProduit(order:str=None, order_type:OrderType = OrderType.DESC, limit:int=None, offset:int=None) -> list[Produit]:
    filter = GetAllFilter()
    filter.order = order
    filter.order_type = order_type
    filter.limit = limit
    filter.offset = offset
    prs = InMemoryStorage.for_type(Produit).get_all(filter)
    return prs

@router.patch("/{uid}")
def edit_produit(uid: uuid.UUID, item: Produit) -> bool:
    pr = InMemoryStorage.for_type(Produit).get(uid)
    if not pr:
        return False
    update_data = item.dict(exclude_unset=True)
    InMemoryStorage.for_type(Produit).update(uid, pr.copy(update=update_data))
    return True

@router.post("/")
def add_produit(produit: Produit) -> uuid.UUID:
    new_uuid = InMemoryStorage.for_type(Produit).create(produit)
    return new_uuid
