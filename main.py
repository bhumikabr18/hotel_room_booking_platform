from fastapi import FastAPI, HTTPException, Query
from typing import Optional, List
from app.models import HotelCreate, RoomCreate, BookRequest, Hotel, Room, Booking
from app.store import store
from app.booking import book_room

app = FastAPI(title="Hotel Room Booking Platform")

@app.post("/hotels", response_model=Hotel)
def create_hotel(payload: HotelCreate):
    return store.add_hotel(name=payload.name, city=payload.city)

@app.post("/rooms", response_model=Room)
def create_room(payload: RoomCreate):
    if payload.hotel_id not in store.hotels:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return store.add_room(hotel_id=payload.hotel_id, room_type=payload.room_type, price=payload.price)

@app.get("/search", response_model=List[Hotel])
def search(city: Optional[str] = Query(default=None), name: Optional[str] = Query(default=None)):
    return store.search_hotels(city=city, name=name)

@app.post("/book", response_model=Booking)
def book(payload: BookRequest):
    if payload.room_id not in store.rooms:
        raise HTTPException(status_code=404, detail="Room not found")
    b = book_room(room_id=payload.room_id, guest=payload.guest,
                  start_date=payload.start_date, end_date=payload.end_date)
    if b is None:
        raise HTTPException(status_code=409, detail="Overlapping booking or invalid date range")
    return b

# Dev utility to simulate many hotels for search perf testing
@app.post("/dev/simulate")
def simulate(count: int = 1_000_000):
    created = store.simulate_hotels(count=count)
    return {"created": created}

@app.get("/")
def root():
    return {"message": "Hotel Booking API is running 🚀. Visit /docs for API documentation."}

