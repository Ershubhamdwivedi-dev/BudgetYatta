# ✈️ BudgetYatta — AI Travel Planner

BudgetYatta is a mini AI-powered travel planning application.

Users can enter their destination, travel duration, number of travellers,
budget, accommodation preference and travel interests.

The application generates a day-by-day travel itinerary and saves the trip
in a database.

---

## Features

- Travel planning form
- AI-generated itinerary
- Budget-based planning
- Day-by-day itinerary
- Expense breakdown
- SQLite database
- Previous trips
- View saved trips
- Delete trips
- FastAPI backend
- Streamlit frontend
- OpenAI API integration
- Mock fallback when AI API is unavailable
- Deployment ready

---

## Tech Stack

### Frontend

Streamlit

### Backend

Python
FastAPI

### Database

SQLite
SQLAlchemy

### AI

OpenAI API

### Deployment

Render / Streamlit Cloud

---

## Architecture

User

↓

Streamlit Frontend

↓

FastAPI Backend

↓

AI Service

↓

OpenAI API

↓

SQLite Database

↓

FastAPI

↓

Streamlit Frontend

---

## Project Structure

BudgetYatta/

backend/

- main.py
- database.py
- models.py
- schemas.py
- ai_service.py

frontend/

- app.py
- api.py
- styles.py

data/

- budgetyatta.db

---

## Run Locally

### 1. Clone repository

git clone YOUR_GITHUB_REPOSITORY

cd BudgetYatta

---

### 2. Create virtual environment

python -m venv venv

Activate on Windows:

venv\Scripts\activate

---

### 3. Install dependencies

pip install -r requirements.txt

---

### 4. Configure environment

Create a `.env` file.

Add:

OPENAI_API_KEY=your_api_key

OPENAI_MODEL=gpt-4o-mini

BACKEND_URL=http://127.0.0.1:8000

---

## Start Backend

Run:

uvicorn backend.main:app --reload

Backend will run at:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

---

## Start Frontend

Open another terminal.

Run:

cd frontend

streamlit run app.py

Frontend will run at:

http://localhost:8501

---

## AI Fallback

If OPENAI_API_KEY is not available or the AI API fails,
BudgetYatta automatically generates a mock itinerary.

This makes the application usable for development and demonstration
without requiring a paid AI API.

---

## Database

The application uses SQLite with SQLAlchemy.

Each trip stores:

- Trip ID
- Destination
- Duration
- Travellers
- Budget
- Accommodation
- Interests
- Generated itinerary
- Estimated cost
- Created date

---

## AI Development Tools

AI tools were used during development for:

- Code generation assistance
- Debugging
- API structure
- UI ideas
- Prompt design
- Documentation assistance

The application structure, integration, configuration and final
implementation were reviewed and modified as part of the development
process.

---

## Assumptions

- Travel costs are approximate.
- AI-generated information should be verified before real travel.
- The application is a technical demonstration and not a booking platform.
- SQLite is used for simple persistence.

---

## Limitations

- No hotel or flight booking.
- No real-time travel pricing.
- No authentication.
- No live maps integration.
- AI-generated costs may not reflect current market prices.

---

## Future Improvements

- User authentication
- Google Maps integration
- Hotel API
- Flight API
- Real-time weather
- Currency conversion
- Trip editing
- Regenerate itinerary
- Mobile-first UI
- PostgreSQL/Supabase
- Caching