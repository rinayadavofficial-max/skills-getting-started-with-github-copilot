import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import app, activities


client = TestClient(app)


def test_unregister_participant_from_activity():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Ensure the student is not already present before the test.
    if email in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].remove(email)

    signup_response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert signup_response.status_code == 200

    unregister_response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    assert unregister_response.status_code == 200
    assert email not in activities[activity_name]["participants"]
