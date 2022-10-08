import pytest
from routes_api_service.const import RATES_URL


def test_correct(app):
    expected = b'[{"average_price":1112,"day":"2016-01-01"},{"average_price":1112,"day":"2016-01-02"},{"average_price":null,"day":"2016-01-03"}]\n'
    with app.test_client() as client:
        response = client.get(
            RATES_URL,
            query_string=dict(
                date_from="2016-01-01",
                date_to="2016-01-10",
                origin="CNSGH",
                destination="north_europe_main",
            ),
        )
    assert 200 == response.status_code
    assert expected == response.data


@pytest.mark.parametrize(
    "query_string",
    [
        dict(date_from="2016-01-01", origin="A", destination="B"),
        dict(date_to="2016-01-01", origin="A", destination="B"),
        dict(date_from="2016-01-01", destination="B"),
    ],
)
def test_missing_arg(app, query_string):
    with app.test_client() as client:
        response = client.get(RATES_URL, query_string=query_string)
    assert 400 == response.status_code
    assert b"field required" in response.data


@pytest.mark.parametrize(
    "query_string",
    [
        dict(
            date_from="207",
            date_to="2016-01-10",
            origin="A",
            destination="B",
        ),
        dict(
            date_from="2016-01-01",
            date_to="2016A-01-10",
            origin="A",
            destination="B",
        ),
    ],
)
def test_wrong_data(app, query_string):
    with app.test_client() as client:
        response = client.get(RATES_URL, query_string=query_string)
    assert 400 == response.status_code
    assert b"does not match format" in response.data


def test_almost_eternoty(app):
    with app.test_client() as client:
        response = client.get(
            RATES_URL,
            query_string=dict(
                date_from="2016-01-01",
                date_to="99999999-01-10",
                origin="CNSGH",
                destination="north_europe_main",
            ),
        )
    assert 400 == response.status_code
    assert b"does not match format" in response.data
