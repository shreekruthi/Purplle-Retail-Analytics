from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_metrics_endpoint():

    response = client.get(
        "/stores/ST1008/metrics"
    )

    assert response.status_code == 200

    data = response.json()

    assert "unique_visitors" in data
    assert "total_sessions" in data
    assert "conversion_rate" in data
    assert "avg_session_minutes" in data
    assert "queue_depth" in data