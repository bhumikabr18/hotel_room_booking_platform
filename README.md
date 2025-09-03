# Hotel Room Booking Platform (In-Memory, FastAPI)

Implements Hotels, Rooms, in-memory Search, and a Booking system that prevents double-booking, plus tests.

## Tech
- **FastAPI** (HTTP API)
- **In-memory** lists/dicts with simple indices
- **Thread-safe** booking via per-room locks
- **pytest** tests including a simultaneous-booking scenario

## Setup

python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt


## Run the API

uvicorn main:app --reload

It starts at `http://127.0.0.1:8000/docs` (Swagger UI).

## API Overview

- **POST /hotels** – Create a hotel
- **POST /rooms** – Create a room under a hotel
- **POST /book** – Book a room for a date range (prevents overlaps)
- **GET /search** – Search hotels by `city` and/or `name`

## Simulating Large Datasets (1M Hotels)
We provide a script function to _simulate_ 1M hotel entries and index them, without running it in tests by default.

You can hit:

curl -X POST "http://127.0.0.1:8000/dev/simulate?count=1000000"

> Be mindful: generating 1M in-memory entries uses RAM and CPU; try smaller numbers first (e.g., 100k).

## Tests
Run all tests:

pytest -q


### Tests Included
1. **Simultaneous Booking** – Two threads attempt to book the same room overlap; only one succeeds.
2. **Edge Booking** – Same check-in and check-out (no nights) should succeed (treated as [start, end) interval).
3. **Search Tests** – Search by city and name returns expected matches.

## Notes
- Time windows use half-open intervals **[start, end)** to avoid fencepost errors.
- Booking overlap is detected if **start < existing_end and end > existing_start**.
- We keep a lock per room to ensure atomicity under concurrent requests.
