from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == (
        "Bulk Certificate Generator API is running"
    )


def test_create_generation_job():
    data = {
        "event_name": "Python Workshop",
        "event_date": "2026-10-10",
        "recipients": [
            {
                "name": "Test User",
                "email": "test@example.com"
            }
        ]
    }

    response = client.post("/jobs", json=data)

    assert response.status_code == 200

    result = response.json()

    assert result["total"] == 1
    assert result["successful"] == 1
    assert result["failed"] == 0
    assert result["status"] == "completed"


def test_invalid_email():
    data = {
        "event_name": "Python Workshop",
        "event_date": "2026-10-10",
        "recipients": [
            {
                "name": "Test User",
                "email": "invalid-email"
            }
        ]
    }

    response = client.post("/jobs", json=data)

    assert response.status_code == 422


def test_job_status():
    data = {
        "event_name": "Testing Event",
        "event_date": "2026-10-10",
        "recipients": [
            {
                "name": "Status User",
                "email": "status@example.com"
            }
        ]
    }

    response = client.post("/jobs", json=data)

    job_id = response.json()["job_id"]

    status_response = client.get(
        f"/jobs/{job_id}"
    )

    assert status_response.status_code == 200

    result = status_response.json()

    assert result["job_id"] == job_id
    assert result["status"] == "completed"
    assert result["total"] == 1


def test_get_certificate():
    data = {
        "event_name": "Certificate Test",
        "event_date": "2026-10-10",
        "recipients": [
            {
                "name": "Certificate User",
                "email": "certificate@example.com"
            }
        ]
    }

    response = client.post("/jobs", json=data)

    job_id = response.json()["job_id"]

    status_response = client.get(
        f"/jobs/{job_id}"
    )

    assert status_response.status_code == 200
def test_individual_certificate_failure(monkeypatch):

    from app import routes

    def fake_generator(
        recipient_name,
        event_name,
        event_date,
        certificate_id
    ):
        if recipient_name == "Fail User":
            raise Exception("Certificate generation failed")

        return f"certificates/test_{certificate_id}.pdf"

    monkeypatch.setattr(
        routes,
        "generate_certificate",
        fake_generator
    )

    data = {
        "event_name": "Failure Test",
        "event_date": "2026-10-10",
        "recipients": [
            {
                "name": "Good User",
                "email": "good@example.com"
            },
            {
                "name": "Fail User",
                "email": "fail@example.com"
            }
        ]
    }

    response = client.post("/jobs", json=data)

    assert response.status_code == 200

    result = response.json()

    assert result["total"] == 2
    assert result["successful"] == 1
    assert result["failed"] == 1
    assert result["status"] == "completed"

    