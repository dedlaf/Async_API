from http import HTTPStatus

import pytest

pytestmark = pytest.mark.asyncio


async def test_get_review(http_session_get) -> None:
    body, headers, status, cookies = await http_session_get("/mongo/reviews/")
    assert status == HTTPStatus.OK


async def test_create_review(http_session_post) -> None:
    create_user_dict = {
        "user_id": "example_id",
        "movie_id": "example_id",
        "text": "example_text",
        "author": "example_author",
        "user_rating": 10,
    }
    body, headers, status, cookies = await http_session_post(
        "/mongo/reviews/", json=create_user_dict
    )
    assert status == HTTPStatus.OK


async def test_update_review(http_session_put) -> None:
    from ..conftest import review

    review_id = str(review["_id"])
    review1 = {"text": "some text", "user_rating": 10}
    body, headers, status, cookies = await http_session_put(
        f"/mongo/reviews/{review_id}", data=review1
    )

    assert status == HTTPStatus.OK


async def test_delete_review(http_session_delete) -> None:
    from ..conftest import review

    review_id = str(review["_id"])
    body, headers, status, cookies = await http_session_delete(
        f"/mongo/reviews/{review_id}"
    )
    assert status == HTTPStatus.OK
