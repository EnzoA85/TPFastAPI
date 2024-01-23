from fastapi import FastAPI

from ..route import facture
from ..route import reservation
from ..route import client
from ..route import user
from ..route import chambre
from ..route import produit

# Début de l'app

app = FastAPI()

app.include_router(facture.app)
app.include_router(reservation.app)
app.include_router(client.app)
app.include_router(user.app)
app.include_router(chambre.app)
app.include_router(produit.app)