import pytest

from src.Services.RedditTwitterDataAPI \
    .reddit_twitter_data_api_with_sqlite import app



@pytest.fixture
def client():
    # Prepare before your test
    with app.test_client() as client:
        # Give control to your test
        yield client
