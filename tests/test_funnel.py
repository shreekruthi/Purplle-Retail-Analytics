from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_funnel_endpoint():

    response = client.get(
        "/stores/ST1008/funnel"
    )

    assert response.status_code == 200

    data = response.json()

    assert "visitors" in data

    assert "zone_visitors" in data

    assert "queue_visitors" in data

    assert "converted_visitors" in data