from fastapi import FastAPI

from ..route import facture
from ..route import reservation
from ..route import client
from ..route import user
from ..route import chambre
from ..route import produit

# Début de l'app

app = FastAPI()

app.include_router(facture.router)
app.include_router(reservation.router)
app.include_router(client.router)
app.include_router(user.router)
app.include_router(chambre.router)
app.include_router(produit.router)