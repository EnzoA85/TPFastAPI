import uuid as uuid

from fastapi import APIRouter

app = APIRouter()

@app.get("/chambres")
def get_lesChambres():
    return "TOTO"

@app.get("/chambre/{chambre_uuid}")
def get_uneChambre(chambre_uuid: uuid.UUID):
    return "TOTO"