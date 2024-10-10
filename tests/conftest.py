import pytest
import base64

from fastapi.testclient import TestClient

from export.entrypoints.app import app
from export.settings import settings


@pytest.fixture(scope="module")
def api_client():
    credentials = f"{settings.username}:{settings.password}"
    b64_encoded_creds = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    return TestClient(app, headers={"Authorization": f"Basic {b64_encoded_creds}"})
