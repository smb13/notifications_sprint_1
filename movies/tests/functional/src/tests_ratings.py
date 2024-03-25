import pytest

pytestmark = [
    pytest.mark.asyncio(),
]


async def test_ratings(make_get_request, make_post_request, make_delete_request):
    movie_id = '0dbfdff6-1bd9-49be-b9b0-27f4d4503904'

    assert await make_delete_request(
        f"/api/v1/ratings/{movie_id}/",
        service='ratings'
    ) is None

    assert await make_post_request(
        f"/api/v1/ratings/{movie_id}/like",
        service='ratings'
    ) is None

    assert await make_get_request(
        f"/api/v1/ratings/{movie_id}",
        service='ratings'
    ) == {"likes": 1, "dislikes": 0, "average": 10, "rating": 10, "total": 1}

    assert await make_post_request(
        f"/api/v1/ratings/{movie_id}/dislike",
        service='ratings'
    ) is None

    assert await make_get_request(
        f"/api/v1/ratings/{movie_id}",
        service='ratings'
    ) == {"likes": 0, "dislikes": 1, "average": 1, "rating": 1, "total": 1}

    assert await make_post_request(
        f"/api/v1/ratings/{movie_id}/5",
        service='ratings'
    ) is None

    assert await make_get_request(
        f"/api/v1/ratings/{movie_id}",
        service='ratings'
    ) == {"likes": 0, "dislikes": 0, "average": 5, "rating": 5, "total": 1}

    assert await make_delete_request(
        f"/api/v1/ratings/{movie_id}/",
        service='ratings'
    ) is None

    assert await make_get_request(
        f"/api/v1/ratings/{movie_id}",
        service='ratings'
    ) == {"likes": 0, "dislikes": 0, "average": None, "rating": 0, "total": 1}
