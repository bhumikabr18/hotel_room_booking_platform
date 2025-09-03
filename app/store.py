from __future__ import annotations
from typing import Dict, List, Optional
from threading import Lock
from app.models import Hotel, Room, Booking

class Store:
    def __init__(self) -> None:
        # In-memory stores
        self.hotels: Dict[int, Hotel] = {}
        self.rooms: Dict[int, Room] = {}
        self.bookings: Dict[int, Booking] = {}

        # Simple indices
        self.hotels_by_city: Dict[str, List[int]] = {}
        self.hotels_by_name: Dict[str, List[int]] = {}

        # ID counters
        self._hotel_id = 0
        self._room_id = 0
        self._booking_id = 0

        # Per-room locks for booking
        self._room_locks: Dict[int, Lock] = {}

    # --- ID helpers ---
    def next_hotel_id(self) -> int:
        self._hotel_id += 1
        return self._hotel_id

    def next_room_id(self) -> int:
        self._room_id += 1
        return self._room_id

    def next_booking_id(self) -> int:
        self._booking_id += 1
        return self._booking_id

    def get_room_lock(self, room_id: int) -> Lock:
        if room_id not in self._room_locks:
            self._room_locks[room_id] = Lock()
        return self._room_locks[room_id]

    # --- Hotel ops ---
    def add_hotel(self, name: str, city: str) -> Hotel:
        hid = self.next_hotel_id()
        hotel = Hotel(id=hid, name=name, city=city, room_ids=[])
        self.hotels[hid] = hotel

        self.hotels_by_city.setdefault(city.lower(), []).append(hid)
        self.hotels_by_name.setdefault(name.lower(), []).append(hid)
        return hotel

    def add_room(self, hotel_id: int, room_type: str, price: float) -> Room:
        assert hotel_id in self.hotels, "Hotel does not exist"
        rid = self.next_room_id()
        room = Room(id=rid, hotel_id=hotel_id, room_type=room_type, price=price)
        self.rooms[rid] = room
        self.hotels[hotel_id].room_ids.append(rid)
        return room

    def list_bookings_for_room(self, room_id: int) -> List[Booking]:
        return [b for b in self.bookings.values() if b.room_id == room_id]

    # --- Booking ops ---
    def add_booking(self, room_id: int, guest: str, start_date, end_date) -> Optional[Booking]:
        # Validate dates
        if end_date < start_date:
            return None
        if end_date == start_date:
            # allow zero-night "booking"
            bid = self.next_booking_id()
            booking = Booking(id=bid, room_id=room_id, guest=guest,
                              start_date=start_date, end_date=end_date)
            self.bookings[bid] = booking
            return booking

        # Use per-room lock to ensure atomicity
        lock = self.get_room_lock(room_id)
        with lock:
            # Check overlaps (intervals are [start, end))
            existing = self.list_bookings_for_room(room_id)
            for b in existing:
                if (start_date < b.end_date) and (end_date > b.start_date):
                    # overlap detected
                    return None

            # No overlap, create booking
            bid = self.next_booking_id()
            booking = Booking(id=bid, room_id=room_id, guest=guest,
                              start_date=start_date, end_date=end_date)
            self.bookings[bid] = booking
            return booking

    # --- Search ---
    def search_hotels(self, city: Optional[str] = None, name: Optional[str] = None) -> List[Hotel]:
        city_ids = None
        name_ids = None

        if city:
            city_ids = set(self.hotels_by_city.get(city.lower(), []))
        if name:
            name_ids = set(self.hotels_by_name.get(name.lower(), []))

        if city and name:
            ids = city_ids.intersection(name_ids)
        elif city:
            ids = city_ids or set()
        elif name:
            ids = name_ids or set()
        else:
            ids = set(self.hotels.keys())

        return [self.hotels[i] for i in ids]

    # --- Dev utility: simulate many hotels ---
    def simulate_hotels(self, count: int = 1_000_000, cities: Optional[list] = None) -> int:
        """
        Simulate a large number of hotels to test search performance.
        Avoids creating rooms to keep memory usage lower.
        """
        if cities is None:
            cities = ["goa", "shimla", "mumbai", "delhi", "chennai",
                      "bengaluru", "pune", "kolkata", "jaipur", "hyderabad"]
        created = 0
        for i in range(count):
            name = f"Hotel-{i}"
            city = cities[i % len(cities)]
            self.add_hotel(name=name, city=city)
            created += 1
        return created

# Global singleton store
store = Store()
