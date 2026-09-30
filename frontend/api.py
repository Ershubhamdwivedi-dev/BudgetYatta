import os
import requests
import os

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
).rstrip("/")


def create_trip(payload):
    response = requests.post(
        f"{BACKEND_URL}/trips",
        json=payload,
        timeout=120
    )

    if not response.ok:
        try:
            detail = response.json()
            raise Exception(
                f"Backend Error {response.status_code}: {detail}"
            )
        except ValueError:
            response.raise_for_status()

    return response.json()


def get_trips():
    response = requests.get(
        f"{BACKEND_URL}/trips",
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    # Backend agar {"trips": [...]} return kare
    if isinstance(data, dict) and "trips" in data:
        return data["trips"]

    # Backend direct list return kare
    if isinstance(data, list):
        return data

    return []


def get_trip(trip_id):
    response = requests.get(
        f"{BACKEND_URL}/trips/{trip_id}",
        timeout=30
    )

    if not response.ok:
        try:
            detail = response.json()
            raise Exception(
                f"Backend Error {response.status_code}: {detail}"
            )
        except ValueError:
            response.raise_for_status()

    return response.json()


def delete_trip(trip_id):
    response = requests.delete(
        f"{BACKEND_URL}/trips/{trip_id}",
        timeout=30
    )

    response.raise_for_status()

    return response.json()