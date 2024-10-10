import requests
from fastapi.testclient import TestClient


def test_export_endpoint(api_client: TestClient):
    response = api_client.get(
        "/export",
        params={"queue_id": 1355018, "annotation_id": 4379183},
    )

    assert response.status_code == 200
    assert response.json()["success"] is True

    postbin_request_url = response.headers["x-postbin-request-url"]
    resp = requests.get(postbin_request_url)
    assert resp.status_code == 200
    assert resp.json()["body"]["content"] is not None

    # TODO assert data
