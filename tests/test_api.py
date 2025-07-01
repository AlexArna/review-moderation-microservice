from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

# ---- TestClient will allow us to hit the FastAPI endpoints in-memory ----
client = TestClient(app)

# ---- Create a fake DB session dependency to avoid touching a real DB ----
def fake_get_db():
    class DummySession:
        def add(self, x): pass
        def commit(self): pass
        def refresh(self, x):
            # Simulate DB-generated fields
            x.id = 123
            x.timestamp = None
        def query(self, x): return []
    yield DummySession()

# ---- Patch the Kafka producer so it doesn't connect to a real broker ----
fake_producer = MagicMock()
fake_producer.send = MagicMock(return_value=None)
fake_producer.flush = MagicMock(return_value=None)

# ---- Patch both DB and Kafka dependencies in app.main ----
@patch("app.main.get_kafka_producer", return_value=fake_producer)
@patch("app.main.get_db", fake_get_db)
def test_post_review_accept(mock_kafka):
    # This test will POST a review and expect an "accept" decision.
    response = client.post("/reviews", json={
        "user_id": "usr1",
        "business_id": "bus1",
        "text": "Excellent meal and service!"
    })
    assert response.status_code == 200
    assert response.json()["decision"] == "accept"

@patch("app.main.get_kafka_producer", return_value=fake_producer)
@patch("app.main.get_db", fake_get_db)
def test_post_review_profane(mock_kafka):
    # This test will POST a profane review and expect a "reject" decision.
    response = client.post("/reviews", json={
        "user_id": "usr2",
        "business_id": "bus2",
        "text": "This food is damn awful!"
    })
    assert response.status_code == 200
    assert response.json()["decision"] == "reject"

@patch("app.main.get_producer", return_value=fake_producer)
@patch("app.main.get_db", fake_get_db)
def test_post_review_spam_short(mock_kafka):
    # This test will POST a too-short review and expect a "flag" decision.
    response = client.post("/reviews", json={
        "user_id": "usr3",
        "business_id": "bus3",
        "text": "Ok"
    })
    assert response.status_code == 200
    assert response.json()["decision"] == "flag"

@patch("app.main.get_kafka_producer", return_value=fake_producer)
@patch("app.main.get_db", fake_get_db)
def test_root_endpoint(mock_kafka):
    # Simple GET to the root endpoint
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"].startswith("Review Moderation Microservice")