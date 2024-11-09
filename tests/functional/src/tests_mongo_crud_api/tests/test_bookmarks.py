from http import HTTPStatus

import pytest

pytestmark = pytest.mark.asyncio


async def test_get_bookmark(http_session_get) -> None:
    from ..conftest import user

    user_id = str(user["_id"])
    body, headers, status, cookies = await http_session_get(
        f"/mongo/bookmarks/{user_id}"
    )
    assert status == HTTPStatus.OK


async def test_create_bookmark(http_session_post) -> None:
    from ..conftest import user

    data = {"user_id": str(user["_id"]), "movie_id": "672f43bf84b967fc136b5deb"}
    body, headers, status, cookies = await http_session_post(
        "/mongo/bookmarks/", json=data
    )
    assert status == HTTPStatus.OK


async def test_delete_bookmark(http_session_delete) -> None:
    from ..conftest import user

    user_id = str(user["_id"])
    data = {"user_id": user_id, "movie_id": "672f43bf84b967fc136b5deb"}
    body, headers, status, cookies = await http_session_delete(
        f"/mongo/bookmarks/", data=data
    )
    assert status == HTTPStatus.OK
