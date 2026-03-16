"""
Tests for the Mergington High School API
Using AAA (Arrange-Act-Assert) structure
"""

import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import sys

# Ensure src is on the path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    initial_state = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"],
        },
        "Soccer Team": {
            "description": "Join the school soccer team and compete in matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["alex@mergington.edu", "lucas@mergington.edu"],
        },
        "Basketball Club": {
            "description": "Practice basketball skills and play friendly games",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 15,
            "participants": ["mia@mergington.edu", "noah@mergington.edu"],
        },
        "Art Workshop": {
            "description": "Explore painting, drawing, and creative arts",
            "schedule": "Mondays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["ava@mergington.edu", "liam@mergington.edu"],
        },
        "Drama Club": {
            "description": "Act, direct, and participate in school plays",
            "schedule": "Fridays, 3:30 PM - 5:30 PM",
            "max_participants": 20,
            "participants": ["ella@mergington.edu", "jack@mergington.edu"],
        },
        "Math Olympiad": {
            "description": "Prepare for math competitions and solve challenging problems",
            "schedule": "Thursdays, 4:00 PM - 5:00 PM",
            "max_participants": 10,
            "participants": ["grace@mergington.edu", "henry@mergington.edu"],
        },
        "Science Club": {
            "description": "Conduct experiments and explore scientific topics",
            "schedule": "Wednesdays, 4:00 PM - 5:00 PM",
            "max_participants": 14,
            "participants": ["chloe@mergington.edu", "ben@mergington.edu"],
        },
    }

    activities.clear()
    activities.update(initial_state)
    yield
    activities.clear()
    activities.update(initial_state)


@pytest.fixture
def client():
    return TestClient(app)


class TestGetActivities:
    def test_get_activities_returns_proper_structure(self, client):
        # Arrange
        expected_keys = {"Chess Club", "Programming Class", "Gym Class"}

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        body = response.json()
        assert expected_keys.issubset(set(body.keys()))
        assert isinstance(body["Chess Club"]["participants"], list)


class TestSignup:
    def test_signup_success(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 200
        assert email in activities[activity_name]["participants"]

    def test_signup_duplicate_fails(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 400


class TestRemoveParticipant:
    def test_remove_participant_success(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 200
        assert email not in activities[activity_name]["participants"]

    def test_remove_participant_not_found(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "notfound@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 404
