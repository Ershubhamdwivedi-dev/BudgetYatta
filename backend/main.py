import json

from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from .database import Base
from .database import engine
from .database import get_db

from .models import Trip

from .schemas import (
    TripRequest,
    TripResponse,
    TripListResponse
)

from .ai_service import generate_trip


Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="BudgetYatta API",
    description="AI Travel Planner API",
    version="1.0.0"
)


@app.get("/")
def root():

    return {
        "message": "BudgetYatta API is running",
        "status": "success"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.post(
    "/trips",
    response_model=TripResponse
)
def create_trip(
    request: TripRequest,
    db: Session = Depends(get_db)
):

    if not request.destination.strip():

        raise HTTPException(
            status_code=400,
            detail="Destination is required."
        )

    if not request.interests.strip():

        raise HTTPException(
            status_code=400,
            detail="At least one interest is required."
        )

    generated = generate_trip(
        destination=request.destination,
        duration=request.duration,
        travellers=request.travellers,
        budget=request.budget,
        accommodation=request.accommodation,
        interests=request.interests
    )

    trip = Trip(
        destination=request.destination.strip(),
        duration=request.duration,
        travellers=request.travellers,
        budget=request.budget,
        accommodation=request.accommodation,
        interests=request.interests.strip(),
        itinerary=json.dumps(
            generated
        ),
        estimated_cost=generated[
            "total_estimated_cost"
        ]
    )

    db.add(trip)
    db.commit()
    db.refresh(trip)

    return {
        "id": trip.id,
        "destination": trip.destination,
        "duration": trip.duration,
        "travellers": trip.travellers,
        "budget": trip.budget,
        "accommodation": trip.accommodation,
        "interests": trip.interests,
        "itinerary": generated,
        "estimated_cost": trip.estimated_cost,
        "created_at": trip.created_at
    }


@app.get(
    "/trips",
    response_model=list[TripListResponse]
)
def get_trips(
    db: Session = Depends(get_db)
):

    trips = (
        db.query(Trip)
        .order_by(
            Trip.created_at.desc()
        )
        .all()
    )

    return trips


@app.get(
    "/trips/{trip_id}",
    response_model=TripResponse
)
def get_trip(
    trip_id: int,
    db: Session = Depends(get_db)
):

    trip = (
        db.query(Trip)
        .filter(
            Trip.id == trip_id
        )
        .first()
    )

    if not trip:

        raise HTTPException(
            status_code=404,
            detail="Trip not found."
        )

    return {
        "id": trip.id,
        "destination": trip.destination,
        "duration": trip.duration,
        "travellers": trip.travellers,
        "budget": trip.budget,
        "accommodation": trip.accommodation,
        "interests": trip.interests,
        "itinerary": json.loads(
            trip.itinerary
        ),
        "estimated_cost": trip.estimated_cost,
        "created_at": trip.created_at
    }


@app.delete(
    "/trips/{trip_id}"
)
def delete_trip(
    trip_id: int,
    db: Session = Depends(get_db)
):

    trip = (
        db.query(Trip)
        .filter(
            Trip.id == trip_id
        )
        .first()
    )

    if not trip:

        raise HTTPException(
            status_code=404,
            detail="Trip not found."
        )

    db.delete(trip)
    db.commit()

    return {
        "message": "Trip deleted successfully"
    }