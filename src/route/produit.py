import uuid as uuid
import enum

from fastapi import APIRouter
from pydantic import BaseModel

app = APIRouter(prefix="/produit")

class TypeProduit(enum.StrEnum):
    Boisson = enum.auto()
    Nourriture = enum.auto()
    Menager = enum.auto()

class Produit(BaseModel):
    nom: str
    quantite: int
    prix: float
    type_produit: TypeProduit

class ProduitStorage:

    def __init__(self):
        self._datas: dict[uuid.UUID, Produit] = {}

    def get(self, uuid:uuid.UUID) -> Produit:
        return self._datas.get(uuid)

    def create(self, produit:Produit) -> uuid.UUID:
        new_uuid = uuid.uuid4()
        self._datas[new_uuid] = produit
        return new_uuid

    def get_all(self) -> list[Produit]:
        return list(self._datas.values())

    def update(self, uuid: uuid.UUID, produit: Produit):
        self._datas[uuid] = produit

_storage = ProduitStorage()

@app.get("/")
def get_AllProduit() -> list[Produit]:
    prs = _storage.get_all()
    return prs

@app.get("/{uuid}")
def get_produit(uuid:uuid.UUID) -> Produit:
    pr = _storage.get(uuid)
    if not pr:
        raise ValueError()
    return pr

@app.post("/")
def add_produit(produit: Produit) -> uuid.UUID:
    new_uuid = _storage.create(produit)
    return new_uuid

@app.patch("/{uuid}")
def edit_produit(uuid: uuid.UUID, item: Produit) -> bool:
    pr = _storage.get(uuid)
    if not pr:
        return False
    update_data = item.dict(exclude_unset=True)
    _storage.update(uuid, pr.copy(update=update_data))
    return True