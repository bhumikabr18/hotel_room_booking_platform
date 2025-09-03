# Hotel Room Booking Platform 

A simple Hotel Room Booking Platform built with FastAPI and in-memory storage.
The system supports creating hotels and rooms, booking rooms while preventing double bookings, and searching hotels by city and/or name.

## Features
- Create Hotels and Rooms
- Book Rooms with overlap prevention
- Search Hotels by city or name
- Handles edge cases (same check-in and check-out allowed)
- Simulate large datasets (up to 1M hotels) for performance testing
- Includes automated tests for critical scenarios

## Tech Stack
- Backend: FastAPI (Python)
- Data Storage: In-memory (dicts & lists with indexing)
- Concurrency: Thread locks for preventing race conditions
- Testing: Pytest

## Setup
### Create and activate a virtual environment:
python -m venv venv
### Windows: 
venv\Scripts\activate
### macOS/Linux:
source venv/bin/activate

## Install dependencies
pip install -r requirements.txt

## Run the Application
### Start the server:
uvicorn main:app --reload

## API Access

### API Root (Health Check)
http://127.0.0.1:8000/
→ Returns a simple JSON message confirming the API is running.

### Swagger UI (Interactive API Docs)
http://127.0.0.1:8000/docs
→ Use this to test endpoints (/hotels, /rooms, /book, /search) directly from the browser.

## Simulating Large Datasets (1M Hotels)
We provide a script function to _simulate_ 1M hotel entries and index them, without running it in tests by default.

## API Endpoints
### Hotels
- POST /hotels → Create a new hotel

### Rooms
- POST /rooms → Add a room to a hotel

### Bookings
- POST /book → Book a room (prevents overlaps)

### Search
- GET /search?city=City&name=HotelName → Search hotels

### Dev Utility
- POST /dev/simulate?count=1000000 → Generate mock hotels for testing large datasets

## Running Tests
### Run all test cases with:
pytest -q

## Tests included:

1. Simultaneous Booking → only one booking succeeds
2. Edge Booking → same check-in/out date succeeds
3. Non-overlapping Bookings → both succeed
4. Search Tests → city & name queries return correct results

## Future Enhancements

- Add caching layer (e.g., Redis) for faster search
- Add rate limiting for booking endpoints
- Build a simple frontend (React/HTML) for hotel search and booking
