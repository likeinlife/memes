import uuid

from fastapi import status
from fastapi.testclient import TestClient


def test_get_404(client: TestClient):
    response = client.get(f"/memes/{uuid.uuid4()}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_success(client: TestClient):
    payload = {"text": "some text"}
    files = {"image": ("image.png", b"some image content")}

    response_create = client.post("/memes/", files=files, params=payload)

    assert response_create.status_code == status.HTTP_201_CREATED, response_create.text
    created_id = uuid.UUID(response_create.json()["meme_id"])

    response = client.get(f"/memes/{created_id}/")
    assert response.status_code == status.HTTP_200_OK
