from fastapi import FastAPI, HTTPException, Query, Path
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict
from fastapi.middleware.cors import CORSMiddleware

# PUBLIC_INTERFACE
class GeoPoint(BaseModel):
    """Geographic coordinate for latitude and longitude."""
    lat: float = Field(..., description="Latitude in decimal degrees")
    lng: float = Field(..., description="Longitude in decimal degrees")


# PUBLIC_INTERFACE
class Address(BaseModel):
    """Postal address with optional geolocation."""
    line1: Optional[str] = Field(None, description="Address line 1")
    line2: Optional[str] = Field(None, description="Address line 2")
    city: Optional[str] = Field(None, description="City")
    state: Optional[str] = Field(None, description="State/Region")
    postalCode: Optional[str] = Field(None, description="Postal/ZIP code")
    country: Optional[str] = Field(None, description="Country")
    location: Optional[GeoPoint] = Field(None, description="Geolocation for the address")


# PUBLIC_INTERFACE
class Hotel(BaseModel):
    """Hotel/restaurant entity as per OpenAPI schema."""
    id: str = Field(..., description="Unique hotel id")
    name: str = Field(..., description="Hotel/restaurant display name")
    description: Optional[str] = Field(None, description="Short description")
    cuisines: Optional[List[str]] = Field(default_factory=list, description="List of cuisines")
    rating: float = Field(..., ge=0, le=5, description="Average rating (0-5)")
    ratingCount: Optional[int] = Field(0, description="Number of ratings")
    priceLevel: Optional[int] = Field(None, ge=1, le=4, description="Price level (1-4)")
    isOpen: bool = Field(..., description="Open status")
    location: GeoPoint = Field(..., description="Geolocation for the outlet")
    address: Optional[Address] = Field(None, description="Address")
    etaMinutes: Optional[int] = Field(None, description="Estimated delivery time in minutes")
    imageUrl: Optional[HttpUrl] = Field(None, description="Preview image URL")


# PUBLIC_INTERFACE
class MenuOptionChoice(BaseModel):
    """Choice within a menu option."""
    id: Optional[str] = Field(None, description="Choice id")
    label: Optional[str] = Field(None, description="Choice label")
    priceDelta: Optional[float] = Field(0, description="Additional cost for the choice")


# PUBLIC_INTERFACE
class MenuOption(BaseModel):
    """Configuration option for a menu item (e.g., size, toppings)."""
    name: Optional[str] = Field(None, description="Option group name")
    min: Optional[int] = Field(0, description="Minimum number of selections")
    max: Optional[int] = Field(1, description="Maximum number of selections")
    options: Optional[List[MenuOptionChoice]] = Field(default_factory=list, description="Available choices")


# PUBLIC_INTERFACE
class MenuItem(BaseModel):
    """Menu item as per OpenAPI schema."""
    id: str = Field(..., description="Menu item id")
    hotelId: str = Field(..., description="Associated hotel id")
    name: str = Field(..., description="Item name")
    description: Optional[str] = Field(None, description="Item description")
    price: float = Field(..., ge=0, description="Base price")
    currency: Optional[str] = Field("USD", description="Currency code (e.g., USD)")
    isVeg: Optional[bool] = Field(None, description="Vegetarian flag")
    spicyLevel: Optional[int] = Field(None, ge=0, le=3, description="Spice level (0-3)")
    imageUrl: Optional[HttpUrl] = Field(None, description="Image URL")
    available: Optional[bool] = Field(True, description="Availability flag")
    options: Optional[List[MenuOption]] = Field(default_factory=list, description="Configurable options")


# In-memory dataset for MVP
HOTELS: Dict[str, Hotel] = {
    "h1": Hotel(
        id="h1",
        name="Spice Route",
        description="Authentic Indian cuisine with a modern twist.",
        cuisines=["Indian", "Vegetarian"],
        rating=4.5,
        ratingCount=1630,
        priceLevel=2,
        isOpen=True,
        location=GeoPoint(lat=37.7749, lng=-122.4194),
        address=Address(
            line1="123 Curry Ave",
            city="San Francisco",
            state="CA",
            postalCode="94103",
            country="USA",
            location=GeoPoint(lat=37.7749, lng=-122.4194),
        ),
        etaMinutes=35,
        imageUrl="https://example.com/images/h1.jpg",
    ),
    "h2": Hotel(
        id="h2",
        name="Sushi Zen",
        description="Fresh sushi and sashimi delivered fast.",
        cuisines=["Japanese", "Seafood"],
        rating=4.7,
        ratingCount=980,
        priceLevel=3,
        isOpen=False,
        location=GeoPoint(lat=34.0522, lng=-118.2437),
        address=Address(
            line1="456 Sakura St",
            city="Los Angeles",
            state="CA",
            postalCode="90012",
            country="USA",
            location=GeoPoint(lat=34.0522, lng=-118.2437),
        ),
        etaMinutes=45,
        imageUrl="https://example.com/images/h2.jpg",
    ),
    "h3": Hotel(
        id="h3",
        name="Pasta Palace",
        description="Handmade pasta and sauces.",
        cuisines=["Italian"],
        rating=4.2,
        ratingCount=540,
        priceLevel=2,
        isOpen=True,
        location=GeoPoint(lat=40.7128, lng=-74.0060),
        address=Address(
            line1="789 Roma Rd",
            city="New York",
            state="NY",
            postalCode="10001",
            country="USA",
            location=GeoPoint(lat=40.7128, lng=-74.0060),
        ),
        etaMinutes=30,
        imageUrl="https://example.com/images/h3.jpg",
    ),
}

MENUS: Dict[str, List[MenuItem]] = {
    "h1": [
        MenuItem(
            id="m1",
            hotelId="h1",
            name="Paneer Tikka Masala",
            description="Grilled paneer simmered in creamy tomato sauce.",
            price=12.5,
            currency="USD",
            isVeg=True,
            spicyLevel=1,
            imageUrl="https://example.com/images/m1.jpg",
            available=True,
            options=[
                MenuOption(
                    name="Spice Level",
                    min=1,
                    max=1,
                    options=[
                        MenuOptionChoice(id="m1s0", label="Mild", priceDelta=0),
                        MenuOptionChoice(id="m1s1", label="Medium", priceDelta=0),
                        MenuOptionChoice(id="m1s2", label="Hot", priceDelta=0),
                    ],
                ),
                MenuOption(
                    name="Extras",
                    min=0,
                    max=2,
                    options=[
                        MenuOptionChoice(id="m1e1", label="Extra Paneer", priceDelta=2.0),
                        MenuOptionChoice(id="m1e2", label="Extra Sauce", priceDelta=1.0),
                    ],
                ),
            ],
        )
    ],
    "h2": [
        MenuItem(
            id="m2",
            hotelId="h2",
            name="Salmon Nigiri (6 pc)",
            description="Fresh salmon slices over seasoned rice.",
            price=18.0,
            currency="USD",
            isVeg=False,
            spicyLevel=0,
            imageUrl="https://example.com/images/m2.jpg",
            available=True,
            options=[],
        ),
    ],
    "h3": [
        MenuItem(
            id="m3",
            hotelId="h3",
            name="Spaghetti Carbonara",
            description="Classic Roman recipe with eggs, pecorino, and guanciale.",
            price=14.0,
            currency="USD",
            isVeg=False,
            spicyLevel=0,
            imageUrl="https://example.com/images/m3.jpg",
            available=True,
            options=[],
        ),
        MenuItem(
            id="m4",
            hotelId="h3",
            name="Margherita Pizza",
            description="Tomato, mozzarella, basil, extra virgin olive oil.",
            price=11.0,
            currency="USD",
            isVeg=True,
            spicyLevel=0,
            imageUrl="https://example.com/images/m4.jpg",
            available=True,
            options=[],
        ),
    ],
}

openapi_tags = [
    {"name": "Hotels", "description": "Hotel discovery and details"},
    {"name": "Menus", "description": "Menu browsing for hotels"},
]

app = FastAPI(
    title="Hotel & Menu Service API",
    description="Manages hotel discovery, details, and menus.",
    version="1.0.0",
    openapi_tags=openapi_tags,
)

# Allow CORS for local development; adjust as needed via environment in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# PUBLIC_INTERFACE
@app.get(
    "/hotels",
    response_model=List[Hotel],
    tags=["Hotels"],
    summary="Search hotels",
    description="Search hotels by query, cuisine, or basic location parameters. "
                "For MVP, distance sorting is simulated and not geo-accurate.",
)
def search_hotels(
    q: Optional[str] = Query(default=None, description="Free text query on name/description"),
    lat: Optional[float] = Query(default=None, description="Latitude for search center"),
    lng: Optional[float] = Query(default=None, description="Longitude for search center"),
    radius: Optional[int] = Query(default=5000, description="Search radius in meters (MVP ignored)"),
    cuisine: Optional[str] = Query(default=None, description="Cuisine to filter"),
    ratingMin: Optional[float] = Query(default=None, ge=0, le=5, description="Minimum rating threshold"),
    sort: Optional[str] = Query(default=None, description="Sort by distance|rating|popularity"),
) -> List[Hotel]:
    """
    Returns a list of hotels filtered by provided query params. This MVP uses naive
    in-memory filters:
    - q filters name/description (case-insensitive)
    - cuisine filters by cuisines list
    - ratingMin filters by rating
    - sort accepts: distance (noop), rating (desc), popularity (by ratingCount desc)
    """
    results = list(HOTELS.values())

    if q:
        q_lower = q.lower()
        results = [
            h for h in results
            if q_lower in h.name.lower() or (h.description and q_lower in h.description.lower())
        ]

    if cuisine:
        c_lower = cuisine.lower()
        results = [h for h in results if any(c_lower in cu.lower() for cu in (h.cuisines or []))]

    if ratingMin is not None:
        results = [h for h in results if h.rating >= ratingMin]

    if sort == "rating":
        results.sort(key=lambda h: (h.rating, h.ratingCount or 0), reverse=True)
    elif sort == "popularity":
        results.sort(key=lambda h: (h.ratingCount or 0, h.rating), reverse=True)
    elif sort == "distance":
        # Placeholder: real implementation would compute distance from (lat, lng).
        pass

    return results


# PUBLIC_INTERFACE
@app.get(
    "/hotels/{hotelId}",
    response_model=Hotel,
    tags=["Hotels"],
    summary="Get hotel by id",
    description="Fetch a single hotel by its identifier.",
    responses={
        404: {"description": "Not found"},
    },
)
def get_hotel(
    hotelId: str = Path(..., description="Hotel identifier"),
) -> Hotel:
    """
    Retrieve details for a specific hotel.
    Raises 404 if hotel is not found.
    """
    hotel = HOTELS.get(hotelId)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return hotel


# PUBLIC_INTERFACE
@app.get(
    "/hotels/{hotelId}/menu",
    response_model=List[MenuItem],
    tags=["Menus"],
    summary="Get menu for a hotel",
    description="Returns the list of menu items for the given hotel.",
)
def get_hotel_menu(
    hotelId: str = Path(..., description="Hotel identifier"),
) -> List[MenuItem]:
    """
    Retrieve menu items for the provided hotel id.
    Returns empty list if hotel exists but has no menu. Raises 404 if hotel not found.
    """
    if hotelId not in HOTELS:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return MENUS.get(hotelId, [])


# PUBLIC_INTERFACE
@app.get(
    "/",
    include_in_schema=False,
)
def root():
    """Health/info endpoint."""
    return {"service": "Hotel&MenuService", "status": "ok", "version": "1.0.0"}
