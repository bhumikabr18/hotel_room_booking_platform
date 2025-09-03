from app.store import store
from app.search import search_hotels

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

def test_search_by_city_and_name():
    h1 = store.add_hotel("Oceanview", "Goa")
    h2 = store.add_hotel("Mountain Inn", "Shimla")
    res_by_city = search_hotels(city="Goa")
    res_by_name = search_hotels(name="Oceanview")
    assert len(res_by_city) == 1
    assert len(res_by_name) == 1
    assert res_by_city[0].id == h1.id
    assert res_by_name[0].id == h1.id

def test_search_by_city_only_multiple():
    store.add_hotel("Sea Breeze", "Goa")
    store.add_hotel("Goa Grand", "Goa")
    res = search_hotels(city="Goa")
    # We now have 3 in Goa
    assert len(res) == 3
