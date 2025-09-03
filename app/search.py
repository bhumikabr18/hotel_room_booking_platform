from __future__ import annotations
from typing import List, Optional
from app.models import Hotel
from app.store import store

def search_hotels(city: Optional[str] = None, name: Optional[str] = None) -> List[Hotel]:
    return store.search_hotels(city=city, name=name)
