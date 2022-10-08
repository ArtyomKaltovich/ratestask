from typing import List

import pytest

from routes_api_service.app import create_app
from routes_api_service.io.rates_repo_abc import RatesRepoABC
from routes_api_service.types import Rate


class RepoMock(RatesRepoABC):
    def get_rates(self, origin, destination, date_from, date_to) -> List[Rate]:
        return [
            {"day": "2016-01-01", "average_price": 1112},
            {"day": "2016-01-02", "average_price": 1112},
            {"day": "2016-01-03", "average_price": None},
        ]


@pytest.fixture
def repo_mock():
    return RepoMock()


@pytest.fixture
def app(repo_mock):
    return create_app(repo_mock, reraise_error=True)
