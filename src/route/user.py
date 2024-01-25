import uuid as uuid

from fastapi import APIRouter
from pydantic import BaseModel
from .storage import InMemoryStorage

router = APIRouter(prefix="/user")

class User(BaseModel):
    login: str
    password: str

@router.post("/")
def add_user(user: User) -> uuid.UUID:
    new_uuid = InMemoryStorage.for_type(User).create(user)
    return new_uuid

@router.patch("/{uid}")
def edit_user(uid: uuid.UUID, item: User) -> bool:
    us = InMemoryStorage.for_type(User).get(uid)
    if not us:
        return False
    update_data = item.dict(exclude_unset=True)
    InMemoryStorage.for_type(User).update(uid, us.copy(update=update_data))
    return True