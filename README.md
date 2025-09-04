# Hotel Room Booking Platform 

A simple Hotel Room Booking Platform built with FastAPI and in-memory storage.
The system supports creating hotels and rooms, booking rooms while preventing double bookings, and searching hotels by city and/or name.

## Problem Statement & Approach
### Problem
- Build an API to manage hotels, rooms, and bookings.
- Prevent double-bookings with concurrent requests.
- Provide search functionality by city and hotel name.
- Handle edge booking cases (same check-in & check-out).
- Support simulation of large datasets (1M hotels).
### Approach
- FastAPI for building APIs.
- In-memory store (dicts & lists) for fast lookups.
- Per-room locks to prevent race conditions and overlapping bookings.
- Indexed search (city & name) for efficient queries.
- Pytest for validating booking and search logic.

## Prerequisites
- Python 3.10+
- pip (Python package manager)
- Virtual environment (recommended)

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
python -m pytest -q

## Test Coverage
1. Simultaneous booking → only one succeeds
2. Edge booking (same check-in/out) → allowed
3. Non-overlapping bookings → both succeed
4. Search by city & name → correct results
5. Large dataset simulation → validates performance

## Explanation of Complex Logic
- Booking Logic: Uses per-room locks + interval overlap detection.
- Search: Indexed dictionaries (city → hotel_ids, name → hotel_ids) for O(1) lookups.
- Concurrency: Thread locks prevent race conditions when two users try to book simultaneously.

## Future Enhancements

- Add caching layer (e.g., Redis) for faster search
- Add rate limiting for booking endpoints
- Build a simple frontend (React/HTML) for hotel search and booking
