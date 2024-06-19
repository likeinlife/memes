import uuid

from fastapi import status
from fastapi.testclient import TestClient


def test_delete_success(client: TestClient):
    payload = {"text": "some text"}
    files = {"image": ("image.png", b"another some image content")}

    response_create = client.post("/memes/", files=files, params=payload)

    assert response_create.status_code == status.HTTP_201_CREATED, response_create.text
    meme_id = uuid.UUID(response_create.json()["meme_id"])

    response_delete = client.delete(f"/memes/{meme_id}/")
    assert response_delete.status_code == status.HTTP_204_NO_CONTENT


def test_delete_not_exists(client: TestClient):
    response_delete = client.delete(f"/memes/{uuid.uuid4()}/")
    assert response_delete.status_code == status.HTTP_404_NOT_FOUND
