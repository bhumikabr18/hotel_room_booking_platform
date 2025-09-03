from __future__ import annotations
from datetime import date
from app.store import store

def book_room(room_id: int, guest: str, start_date: date, end_date: date):
    if room_id not in store.rooms:
        raise ValueError("Room does not exist")
    return store.add_booking(room_id=room_id, guest=guest, start_date=start_date, end_date=end_date)
