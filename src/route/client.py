import uuid as uuid

from fastapi import APIRouter
from pydantic import BaseModel


app = APIRouter(prefix="/client")

class Client(BaseModel):
    nom: str
    prenom: str
    mail: str
    telephone: str
    
class ClientStorage:

    def __init__(self):
        self._datas: dict[uuid.UUID, Client] = {}

    def get(self, uuid:uuid.UUID) -> Client:
        return self._datas.get(uuid)

    def create(self, client:Client) -> uuid.UUID:
        new_uuid = uuid.uuid4()
        self._datas[new_uuid] = client
        return new_uuid

    def get_all(self) -> list[Client]:
        return list(self._datas.values())

    def update(self, uuid: uuid.UUID, client: Client):
        self._datas[uuid] = client

_storage = ClientStorage()

@app.get("/{uuid}")
def get_client(uuid:uuid.UUID) -> Client:
    cl = _storage.get(uuid)
    if not cl:
        raise ValueError()
    return cl

@app.get("/")
def get_AllClient() -> list[Client]:
    cls = _storage.get_all()
    return cls

@app.patch("/{uuid}")
def edit_client(uuid: uuid.UUID, item: Client) -> bool:
    cl = _storage.get(uuid)
    if not cl:
        return False
    update_data = item.dict(exclude_unset=True)
    _storage.update(uuid, cl.copy(update=update_data))
    return True

@app.post("/")
def add_client(client: Client) -> uuid.UUID:
    new_uuid = _storage.create(client)
    return new_uuid