import uuid as uuid

from fastapi import APIRouter

app = APIRouter()

@app.get("/reservations")
def get_lesReservation():
    return "TOTO"

@app.get("/reservations/{reservation_uuid}")
def get_uneReservation(reservation_uuid: uuid.UUID):
    return "TOTO"

@app.post("/addReservation")
def add_reservation():
    return "TOTO"

@app.delete("/deleteReservation/{reservation_uuid}")
def delete_reservation(reservation_uuid: uuid.UUID):
    return "TOTO"

@app.patch("/addReservation/{reservation_uuid}")
def add_reservation(reservation_uuid: uuid.UUID):
    return "TOTO"