import uuid as uuid

from fastapi import APIRouter

app = APIRouter()

@app.post("/addUser")
def add_User():
    return "TOTO"

@app.put("/editUser")
def edit_User():
    return "TOTO"