"""Data models for the travel planner."""
from pydantic import BaseModel


class Recommendation(BaseModel):
    """A single place recommendation in a city."""

    name: str
    category: str
    neighborhood: str
    budget: str
    description: str = ""
    must_order: str = ""
    time_needed: str = ""
    transit: str = ""


class DayBlock(BaseModel):
    """A time block in an itinerary (morning, afternoon, evening)."""

    time_of_day: str
    activity: Recommendation
    meal: Recommendation | None = None


class DayPlan(BaseModel):
    """A single day in an itinerary."""

    day_number: int
    theme: str
    blocks: list[DayBlock]


class Itinerary(BaseModel):
    """A complete multi-day travel itinerary."""

    city: str
    days: list[DayPlan]
    vibe: str
    traveler_budget: str = "$$"


class City(BaseModel):
    """A city with all its recommendation data."""

    name: str
    country: str
    currency: str
    language_tip: str
    neighborhoods: list[dict[str, str]]
    food: list[Recommendation]
    landmarks: list[Recommendation]
    nightlife: list[Recommendation]
    phrases: list[dict[str, str]]
    transit_tips: list[str]
