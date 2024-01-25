import abc
import uuid
from enum import StrEnum, auto
from typing import Protocol, Generic, TypeVar, Type
from pydantic import BaseModel


class OrderType(StrEnum):
    DESC = auto()
    ASC = auto()


T = TypeVar("T", bound=BaseModel)
T2 = TypeVar("T2", bound=BaseModel)


class GetAllFilter(BaseModel):
    order: str = None,
    order_type: OrderType = OrderType.DESC,
    limit: int = None,
    offset: int = None


class UUIDRef(Protocol):
    uid: uuid.UUID


class BaseStorage(Generic[T], abc.ABC):

    def get(self, uid: uuid.UUID) -> T:
        ...

    def create(self, item: T) -> uuid.UUID:
        ...

    def get_all(self, filter: GetAllFilter = None) -> list[T]:
        ...

    def update(self, uuid: uuid.UUID, chambre: T) -> bool:
        ...

    def delete(self, uid: uuid.UUID) -> bool:
        ...


class InMemoryStorage(BaseStorage[T]):

    _in_memory: dict[Type, "InMemoryStorage"] = {}

    @classmethod
    def for_type(cls, type_of: Type[T2]) -> "InMemoryStorage[T2]":
        inst = cls._in_memory.get(type_of)
        if not inst:
            inst = InMemoryStorage()
            cls._in_memory[type_of] = inst
        return inst

    def __init__(self):
        self._datas: dict[uuid.UUID, T] = {}

    def get(self, uid: uuid.UUID) -> T:
        return self._datas.get(uid)

    def create(self, item: T) -> uuid.UUID:
        new_uuid = uuid.uuid4()
        self._datas[new_uuid] = item
        return new_uuid

    def get_all(self, filter: GetAllFilter = None) -> list[T]:
        return list(self._datas.values())

    def update(self, uid: uuid.UUID, item: T) -> bool:
        self._datas[uid] = item
        return True

    def delete(self, uid: uuid.UUID) -> bool:
        return bool(self._datas.pop(uid, None))
