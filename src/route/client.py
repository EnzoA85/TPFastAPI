import uuid as uuid

from fastapi import APIRouter

app = APIRouter()

@app.get("/clients")
def get_lesClients():
    return "TOTO"

@app.get("/client/{client_uuid}")
def get_unClient(client_uuid: uuid.UUID):
    return "TOTO"

@app.put("/editClient")
def edit_client():
    return "TOTO"

@app.post("/addClient")
def add_client():
    return "TOTO"