import pytest

from ted_sws.notice_fetcher.adapters.ted_api import DEFAULT_TED_API_URL
from tests.fakes.fake_repository import FakeNoticeRepository


@pytest.fixture
def fake_notice_storage():
    return FakeNoticeRepository()


@pytest.fixture
def notice_identifier():
    return "067623-2022"


@pytest.fixture
def notice_search_query():
    return {"q": "ND=[067623-2022]"}

@pytest.fixture
def notice_incorrect_search_query():
    return {"q": "ND=067623-20224856"}


@pytest.fixture
def api_end_point():
    return DEFAULT_TED_API_URL


