from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List
from datetime import date

class Hotel(BaseModel):
    id: int
    name: str
    city: str
    room_ids: List[int] = Field(default_factory=list)

class Room(BaseModel):
    id: int
    hotel_id: int
    room_type: str
    price: float

class Booking(BaseModel):
    id: int
    room_id: int
    guest: str
    start_date: date
    end_date: date  # exclusive: booking is [start_date, end_date)

class HotelCreate(BaseModel):
    name: str
    city: str

class RoomCreate(BaseModel):
    hotel_id: int
    room_type: str
    price: float

class BookRequest(BaseModel):
    room_id: int
    guest: str
    start_date: date
    end_date: date
