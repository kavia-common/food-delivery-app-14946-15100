# Hotel & Menu Service (FastAPI) - MVP

This service exposes hotel discovery, details, and menus via REST endpoints, following the provided OpenAPI specification.

OpenAPI spec: `openapi/hotel_menu.yaml`

Endpoints:
- GET /hotels?q=&lat=&lng=&radius=&cuisine=&ratingMin=&sort=
- GET /hotels/{hotelId}
- GET /hotels/{hotelId}/menu

Implementation notes:
- Uses in-memory data structures for hotels and menus.
- Filters include query text (name/description), cuisine, and ratingMin.
- Sorting supports rating (desc) and popularity (ratingCount desc). Distance is a placeholder for MVP.
- CORS is enabled for all origins in development.

Run locally:
1) Create a virtual environment and install dependencies
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

2) Start the server
   uvicorn app.main:app --host 0.0.0.0 --port 8103 --reload

3) Explore the docs
   Swagger UI: http://localhost:8103/docs
   OpenAPI JSON: http://localhost:8103/openapi.json

Environment:
- No required environment variables for the MVP. Do not hardcode configuration; add env variables in future iterations as needed.

Project structure:
- app/main.py         # FastAPI app with endpoints and in-memory data
- openapi/hotel_menu.yaml  # API contract/specification
- requirements.txt    # Python dependencies
- README.md           # This file

Compatibility:
- The Pydantic models and route signatures are aligned with the OpenAPI schemas and parameters present in `openapi/hotel_menu.yaml`.
