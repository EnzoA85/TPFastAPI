import uuid as uuid

from fastapi import APIRouter

app = APIRouter()

@app.get("/factures")
def get_lesFactures():
    return "TOTO"

@app.get("/facture/{facture_uuid}")
def get_uneFacture(facture_uuid: uuid.UUID):
    return "TOTO"