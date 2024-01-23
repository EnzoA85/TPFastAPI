import uuid as uuid

from fastapi import APIRouter
from pydantic import BaseModel

app = APIRouter(prefix="/user")

class User(BaseModel):
    login : str
    password : str
    
class UserStorage:

    def __init__(self):
        self._datas: dict[uuid.UUID, User] = {}

    def get(self, uuid:uuid.UUID) -> User:
        return self._datas.get(uuid)

    def create(self, user:User) -> uuid.UUID:
        new_uuid = uuid.uuid4()
        self._datas[new_uuid] = user
        return new_uuid

    def get_all(self) -> list[User]:
        return list(self._datas.values())

    def update(self, uuid: uuid.UUID, user: User):
        self._datas[uuid] = user
        
_storage = UserStorage()

@app.post("/")
def add_user(user: User) -> uuid.UUID:
    new_uuid = _storage.create(user)
    return new_uuid

@app.patch("/{uuid}")
def edit_user(uuid: uuid.UUID, item: User) -> bool:
    us = _storage.get(uuid)
    if not us:
        return False
    update_data = item.dict(exclude_unset=True)
    _storage.update(uuid, us.copy(update=update_data))
    return True