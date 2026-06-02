from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_anomalies_endpoint():

    response = client.get(
        "/stores/ST1008/anomalies"
    )

    assert response.status_code == 200

    data = response.json()

    assert "anomalies" in data

    assert isinstance(
        data["anomalies"],
        list
    )