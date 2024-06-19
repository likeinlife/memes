import uuid

from fastapi import status
from fastapi.testclient import TestClient


def test_update_success(client: TestClient):
    payload = {"text": "some text"}
    files = {"image": ("image.png", b"another some image content")}

    response_create = client.post("/memes/", files=files, params=payload)

    assert response_create.status_code == status.HTTP_201_CREATED, response_create.text
    meme_id = uuid.UUID(response_create.json()["meme_id"])

    payload = {"text": "another some text"}
    files = {"image": ("image.png", b"another some image content")}
    response_update = client.patch(f"/memes/{meme_id}/", files=files, params=payload)
    assert response_update.status_code == status.HTTP_200_OK, response_update.text

    assert response_update.json()["text"] == payload["text"]


def test_update_not_exists(client: TestClient):
    payload = {"text": "another some text"}
    files = {"image": ("image.png", b"another some image content")}
    response_update = client.patch(f"/memes/{uuid.uuid4()}/", files=files, params=payload)
    assert response_update.status_code == status.HTTP_404_NOT_FOUND, response_update.text
