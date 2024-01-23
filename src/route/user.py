import uuid as uuid

from fastapi import APIRouter

app = APIRouter()

@app.post("/addUser")
def add_User():
    return "TOTO"

@app.put("/editUser/{user_uuid}")
def edit_User(user_uuid: uuid.UUID):
    return "TOTO"