import httpx
import orjson
import pytest
from pydantic import BaseSettings

from routes_api_service.const import RATES_URL


class Settings(BaseSettings):
    url = f"http://127.0.0.1:5000{RATES_URL}"


URL = Settings().url


def test_both_ports():
    result = httpx.get(URL,
                       params=dict(date_from="2016-01-01", date_to="2016-01-03", origin="CNSGH", destination="SESTO"))
    assert result.status_code == 200
    actual = orjson.loads(result.text)
    expected = [{'average_price': '1991.6666666666666667', 'day': '2016-01-01'},
                {'average_price': '1991.3333333333333333', 'day': '2016-01-02'},
                {'average_price': None, 'day': '2016-01-03'}]
    assert actual == expected


def test_dest_region():
    result = httpx.get(URL,
                       params=dict(date_from="2016-01-01", date_to="2016-01-03", origin="CNSGH",
                                   destination="scandinavia"))
    assert result.status_code == 200
    actual = orjson.loads(result.text)
    expected = [{'average_price': '1702.0921052631578947', 'day': '2016-01-01'},
                {'average_price': '1701.9868421052631579', 'day': '2016-01-02'},
                {'average_price': None, 'day': '2016-01-03'}]
    assert actual == expected


def test_origin_region():
    result = httpx.get(URL,
                       params=dict(date_from="2016-01-20", date_to="2016-01-25", destination="FIRAU",
                                   origin="china_east_main"))
    assert result.status_code == 200
    actual = orjson.loads(result.text)
    expected = [{'average_price': '1111.3888888888888889', 'day': '2016-01-20'},
                {'average_price': '1111.0000000000000000', 'day': '2016-01-21'},
                {'average_price': '1110.2777777777777778', 'day': '2016-01-22'},
                {'average_price': '1110.2777777777777778', 'day': '2016-01-23'},
                {'average_price': '1071.3333333333333333', 'day': '2016-01-24'},
                {'average_price': '1045.8333333333333333', 'day': '2016-01-25'}]
    assert actual == expected


def test_both_region():
    result = httpx.get(URL,
                       params=dict(date_from="2016-01-20", date_to="2016-01-21", origin="china_east_main",
                                   destination="scandinavia",
                                   ))
    assert result.status_code == 200
    actual = orjson.loads(result.text)
    expected = [{'average_price': '1365.6586021505376344', 'day': '2016-01-20'},
                {'average_price': '1348.0080645161290323', 'day': '2016-01-21'}]
    assert actual == expected


def test_one_day():
    result = httpx.get(URL,
                       params=dict(date_from="2016-01-19", date_to="2016-01-19", origin="CNSHK", destination="FIHEL",
                                   ))
    assert result.status_code == 200
    actual = orjson.loads(result.text)
    expected = [{'average_price': '1191.6666666666666667', 'day': '2016-01-19'}]
    assert actual == expected


def test_date_to_less_then_from():
    result = httpx.get(URL,
                       params=dict(date_from="2016-01-19", date_to="2016-01-18", origin="CNSHK", destination="FIHEL",
                                   ))
    assert result.status_code == 200
    actual = orjson.loads(result.text)
    expected = []
    assert actual == expected


def test_very_big_date_range():
    result = httpx.get(URL,
                       params=dict(date_from="0001-01-01", date_to="9999-12-31", origin="CNSHK", destination="FIHEL",
                                   ))
    assert result.status_code == 200
