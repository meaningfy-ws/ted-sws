import datetime

from pytest_bdd import scenario, given, when, then, parsers

from ted_sws.notice_fetcher.adapters.ted_api import TedAPIAdapter, TedRequestAPI
from ted_sws.notice_fetcher.services.notice_fetcher import NoticeFetcher


@scenario('test_search_queries.feature', 'Get all notices for the past period')
def test_get_notices_for_past_period():
    """Get all notices for the past period"""


@given("a TED REST API search endpoint")
def step_impl(api_end_point):
    return api_end_point


@given(parsers.parse("search query over {start} to {end} period"), target_fixture="dates")
def step_impl(start, end):
    start_date = datetime.datetime.strptime(start, "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(end, "%Y-%m-%d").date()
    return start_date, end_date


@when("the call to the API is executed", target_fixture="api_call")
def step_impl(dates, notice_storage):
    start_date, end_date = dates
    NoticeFetcher(notice_repository=notice_storage,
                  ted_api_adapter=TedAPIAdapter(request_api=TedRequestAPI())).fetch_notices_by_date_range(
        start_date=start_date, end_date=end_date)
    return list(notice_storage.list())


@then("search result set is returned", target_fixture="search_result")
def step_impl(api_call):
    return api_call


@then(parsers.parse("the expected number of result items is between {min} and {max}"))
def step_impl(min, max, search_result):
    print(len(search_result))
    assert int(min) < len(search_result) < int(max)
