from http import HTTPStatus

import pytest

pytestmark = pytest.mark.asyncio


async def test_get_users(http_session_get) -> None:
    body, headers, status, cookies = await http_session_get("/mongo/users/")
    assert status == HTTPStatus.OK


async def test_create_user(http_session_post) -> None:
    create_user_dict = {
        "name": "name",
        "email": "email@mail.ru",
        "age": 23,
        "bookmarks": [],
    }
    body, headers, status, cookies = await http_session_post(
        "/mongo/users/", json=create_user_dict
    )
    assert status == HTTPStatus.OK


async def test_update_user(http_session_put) -> None:
    from ..conftest import user

    user_id = str(user["_id"])
    user1 = {
        "name": "example_name",
        "email": "example_email@mail.ru",
        "age": 24,
        "bookmarks": [],
    }
    body, headers, status, cookies = await http_session_put(
        f"/mongo/users/{user_id}", data=user1
    )

    assert status == HTTPStatus.OK


async def test_delete_user(http_session_delete) -> None:
    from ..conftest import user

    user_id = str(user["_id"])
    body, headers, status, cookies = await http_session_delete(
        f"/mongo/users/users/{user_id}"
    )
    assert status == HTTPStatus.OK
