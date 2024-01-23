import uuid as uuid

from fastapi import APIRouter

app = APIRouter()

@app.get("/produits")
def get_lesProduits():
    return "TOTO"

@app.get("/produit/{produit_uuid}")
def get_unProduit(produit_uuid: uuid.UUID):
    return "TOTO"

@app.post("/addProduit")
def add_produit():
    return "TOTO"

@app.put("/editProduit")
def edit_produit():
    return "TOTO"