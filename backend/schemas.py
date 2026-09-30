from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class TripRequest(BaseModel):

    destination: str = Field(
        min_length=2,
        max_length=150
    )

    duration: int = Field(
        gt=0,
        le=30
    )

    travellers: int = Field(
        gt=0,
        le=50
    )

    budget: float = Field(
        gt=0
    )

    accommodation: str

    interests: str


class Expense(BaseModel):

    category: str

    estimated_cost: float


class DayPlan(BaseModel):

    day: int

    title: str

    places: List[str]

    activities: List[str]

    food: List[str]

    approximate_cost: float


class TripAIResponse(BaseModel):

    summary: str

    days: List[DayPlan]

    expenses: List[Expense]

    total_estimated_cost: float


class TripResponse(BaseModel):

    id: int

    destination: str

    duration: int

    travellers: int

    budget: float

    accommodation: str

    interests: str

    itinerary: TripAIResponse

    estimated_cost: float

    created_at: datetime


class TripListResponse(BaseModel):

    id: int

    destination: str

    duration: int

    travellers: int

    budget: float
    estimated_cost: float
    created_at: datetime