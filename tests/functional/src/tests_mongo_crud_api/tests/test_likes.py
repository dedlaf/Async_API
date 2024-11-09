from http import HTTPStatus

import pytest

pytestmark = pytest.mark.asyncio


async def test_get_like(http_session_get) -> None:
    body, headers, status, cookies = await http_session_get("/mongo/likes/")
    assert status == HTTPStatus.OK


async def test_create_like(http_session_post) -> None:
    movie_id = "672f43bf84b967fc136b5deb"
    create_user_dict = {"movie_id": movie_id, "user_id": "user123123", "rating": 10}
    body, headers, status, cookies = await http_session_post(
        "/mongo/likes/", json=create_user_dict
    )
    assert status == HTTPStatus.OK


async def test_update_like(http_session_put) -> None:
    from ..conftest import like

    movie_id, user_id = str(like["_id"]), next(iter(like["user_ratings"]))

    like1 = {"movie_id": movie_id, "user_id": user_id, "rating": 10}
    body, headers, status, cookies = await http_session_put(
        f"/mongo/likes/", data=like1
    )

    assert status == HTTPStatus.OK


async def test_delete_like(http_session_delete) -> None:
    from ..conftest import like

    movie_id, user_id = str(like["_id"]), next(iter(like["user_ratings"]))
    data = {"movie_id": movie_id, "user_id": user_id}
    body, headers, status, cookies = await http_session_delete(
        f"/mongo/likes/", data=data
    )
    assert status == HTTPStatus.OK
