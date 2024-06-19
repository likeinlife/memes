import uuid

from fastapi import status
from fastapi.testclient import TestClient

from domain import constants


def test_add_success(client: TestClient):
    payload = {"text": "some text"}
    files = {"image": ("image.png", b"another some image content")}

    response_create = client.post("/memes/", files=files, params=payload)

    assert response_create.status_code == status.HTTP_201_CREATED, response_create.text
    assert uuid.UUID(response_create.json()["meme_id"])


def test_add_blank_text_error(client: TestClient):
    payload = {"text": ""}
    files = {"image": ("image.png", b"another some image content")}

    response_create = client.post("/memes/", files=files, params=payload)

    assert response_create.status_code == status.HTTP_400_BAD_REQUEST, response_create.text


def test_add_too_long_text(client: TestClient):
    payload = {"text": "a" * (constants.MAX_TEXT_LEN + 1)}
    files = {"image": ("image.png", b"another some image content")}

    response_create = client.post("/memes/", files=files, params=payload)

    assert response_create.status_code == status.HTTP_400_BAD_REQUEST, response_create.text
