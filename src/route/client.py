import uuid as uuid

from fastapi import APIRouter
from pydantic import BaseModel
from .storage import OrderType, InMemoryStorage, GetAllFilter

router = APIRouter(prefix="/client")

class Client(BaseModel):
    nom: str
    prenom: str
    mail: str
    telephone: str

@router.get("/{uuid}")
def get_unClient(uuid:uuid.UUID) -> Client:
    cl = InMemoryStorage.for_type(Client).get(uuid)
    if not cl:
        raise ValueError()
    return cl

@router.get("/")
def get_allClient(order:str=None, order_type:OrderType = OrderType.DESC, limit:int=None, offset:int=None) -> list[Client]:
    filter = GetAllFilter()
    filter.order = order
    filter.order_type = order_type
    filter.limit = limit
    filter.offset = offset
    cl = InMemoryStorage.for_type(Client).get_all(filter)
    return cl

@router.patch("/{uid}")
def edit_client(uid: uuid.UUID, item: Client) -> bool:
    cl = InMemoryStorage.for_type(Client).get(uid)
    if not cl:
        return False
    update_data = item.dict(exclude_unset=True)
    InMemoryStorage.for_type(Client).update(uid, cl.copy(update=update_data))
    return True

@router.post("/")
def add_user(client: Client) -> uuid.UUID:
    new_uuid = InMemoryStorage.for_type(Client).create(client)
    return new_uuid