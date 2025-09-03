import threading
from datetime import date
from app.store import store
from app.booking import book_room

def setup_module(module):
    # fresh store state for tests (simple reset)
    store.hotels.clear()
    store.rooms.clear()
    store.bookings.clear()
    store.hotels_by_city.clear()
    store.hotels_by_name.clear()
    store._hotel_id = 0
    store._room_id = 0
    store._booking_id = 0
    store._room_locks.clear()

def test_simultaneous_booking():
    # setup: one hotel & one room
    h = store.add_hotel("Oceanview", "Goa")
    r = store.add_room(h.id, "Single", 1000.0)

    # Two threads try to book overlapping dates
    res = {"b1": None, "b2": None}

    def t1():
        res["b1"] = book_room(r.id, "Alice", date(2025,8,2), date(2025,8,4))

    def t2():
        res["b2"] = book_room(r.id, "Bob", date(2025,8,3), date(2025,8,4))

    th1 = threading.Thread(target=t1)
    th2 = threading.Thread(target=t2)
    th1.start(); th2.start()
    th1.join(); th2.join()

    # Exactly one succeeds
    assert (res["b1"] is not None) ^ (res["b2"] is not None)

def test_edge_same_checkin_checkout_succeeds():
    h = store.add_hotel("EdgeHotel", "Shimla")
    r = store.add_room(h.id, "Single", 1200.0)
    # Same start and end -> zero-night booking allowed
    b = book_room(r.id, "Charlie", date(2025,9,1), date(2025,9,1))
    assert b is not None

def test_non_overlapping_bookings_both_succeed():
    h = store.add_hotel("NonOverlap", "Goa")
    r = store.add_room(h.id, "Double", 1500.0)
    b1 = book_room(r.id, "Daisy", date(2025,9,1), date(2025,9,3))
    b2 = book_room(r.id, "Evan",  date(2025,9,3), date(2025,9,5))  # starts when b1 ends
    assert b1 is not None and b2 is not None
