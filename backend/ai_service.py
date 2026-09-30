import json
import os
from typing import Dict

from openai import OpenAI


def create_prompt(
    destination: str,
    duration: int,
    travellers: int,
    budget: float,
    accommodation: str,
    interests: str
):

    return f"""
You are BudgetYatta, an AI travel planner.

Create a practical travel itinerary using these requirements:

Destination: {destination}
Duration: {duration} days
Travellers: {travellers}
Total Budget: INR {budget}
Accommodation: {accommodation}
Interests: {interests}

Important:
- Keep the estimated total cost close to the user's budget.
- Give realistic travel suggestions.
- Consider the number of travellers.
- Include food, activities and transportation.
- Do not exceed the budget unnecessarily.

Return ONLY valid JSON.

Required JSON structure:

{{
  "summary": "short trip summary",
  "days": [
    {{
      "day": 1,
      "title": "Day title",
      "places": ["place 1", "place 2"],
      "activities": ["activity 1", "activity 2"],
      "food": ["food suggestion"],
      "approximate_cost": 1000
    }}
  ],
  "expenses": [
    {{
      "category": "Stay",
      "estimated_cost": 4500
    }},
    {{
      "category": "Food",
      "estimated_cost": 3000
    }},
    {{
      "category": "Transport",
      "estimated_cost": 3000
    }},
    {{
      "category": "Activities",
      "estimated_cost": 2000
    }},
    {{
      "category": "Miscellaneous",
      "estimated_cost": 1000
    }}
  ],
  "total_estimated_cost": 13500
}}
"""


def mock_trip(
    destination: str,
    duration: int,
    travellers: int,
    budget: float,
    accommodation: str,
    interests: str
) -> Dict:

    daily_budget = budget / duration

    days = []

    for day in range(1, duration + 1):

        days.append(
            {
                "day": day,
                "title": f"Explore {destination} - Day {day}",
                "places": [
                    f"Popular attraction in {destination}",
                    f"Local market in {destination}"
                ],
                "activities": [
                    "Local sightseeing",
                    "Photography",
                    "Explore local culture"
                ],
                "food": [
                    "Try local cuisine",
                    "Visit a popular local restaurant"
                ],
                "approximate_cost": round(daily_budget, 2)
            }
        )

    stay = budget * 0.30
    food = budget * 0.20
    transport = budget * 0.20
    activities = budget * 0.20
    misc = budget * 0.10

    return {
        "summary": (
            f"A {duration}-day {destination} trip for "
            f"{travellers} travellers focused on {interests}."
        ),
        "days": days,
        "expenses": [
            {
                "category": "Stay",
                "estimated_cost": round(stay, 2)
            },
            {
                "category": "Food",
                "estimated_cost": round(food, 2)
            },
            {
                "category": "Transport",
                "estimated_cost": round(transport, 2)
            },
            {
                "category": "Activities",
                "estimated_cost": round(activities, 2)
            },
            {
                "category": "Miscellaneous",
                "estimated_cost": round(misc, 2)
            }
        ],
        "total_estimated_cost": round(budget, 2)
    }


def generate_trip(
    destination: str,
    duration: int,
    travellers: int,
    budget: float,
    accommodation: str,
    interests: str
):

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return mock_trip(
            destination,
            duration,
            travellers,
            budget,
            accommodation,
            interests
        )

    try:

        client = OpenAI(
            api_key=api_key
        )

        response = client.chat.completions.create(
            model=os.getenv(
                "OPENAI_MODEL",
                "gpt-4o-mini"
            ),
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional travel "
                        "planning assistant."
                    )
                },
                {
                    "role": "user",
                    "content": create_prompt(
                        destination,
                        duration,
                        travellers,
                        budget,
                        accommodation,
                        interests
                    )
                }
            ],
            temperature=0.7
        )

        content = response.choices[0].message.content

        content = content.replace(
            "```json",
            ""
        ).replace(
            "```",
            ""
        ).strip()

        return json.loads(content)

    except Exception as error:

        print(
            f"AI API failed: {error}"
        )

        return mock_trip(
            destination,
            duration,
            travellers,
            budget,
            accommodation,
            interests
        )