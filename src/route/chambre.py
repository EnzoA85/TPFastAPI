import enum
import uuid as uuid

from fastapi import APIRouter
from pydantic import BaseModel

app = APIRouter(prefix="/chambre")

class TypeRoom(enum.StrEnum):
    SIMPLE = enum.auto()
    DOUBLE = enum.auto()

class Chambre(BaseModel):
    number: int
    price: float
    type_room: TypeRoom

class ChambreFull(Chambre):
    id: uuid.UUID


class ChambreStorage:

    def __init__(self):
        self._datas: dict[uuid.UUID, Chambre] = {}

    def get(self, uuid:uuid.UUID) -> Chambre:
        return self._datas.get(uuid)

    def create(self, chambre:Chambre) -> uuid.UUID:
        new_uuid = uuid.uuid4()
        self._datas[new_uuid] = chambre
        return new_uuid

    def get_all(self) -> list[Chambre]:
        return list(self._datas.values())

    def update(self, uuid: uuid.UUID, chambre: Chambre):
        self._datas[uuid] = chambre

_storage = ChambreStorage()

@app.get("/{uuid}")
def get_chambre(uuid:uuid.UUID) -> Chambre:
    ch = _storage.get(uuid)
    if not ch:
        raise ValueError()
    return ch

@app.get("/")
def get_AllChambre() -> list[Chambre]:
    chs = _storage.get_all()
    return chs

@app.patch("/{uuid}")
def edit_chambre(uuid: uuid.UUID, item: Chambre) -> bool:
    ch = _storage.get(uuid)
    if not ch:
        return False
    update_data = item.dict(exclude_unset=True)
    _storage.update(uuid, ch.copy(update=update_data))
    return True

@app.post("/")
def add_chambre(chambre: Chambre) -> uuid.UUID:
    new_uuid = _storage.create(chambre)
    return new_uuid