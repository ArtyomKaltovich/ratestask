import abc
from typing import List

from routes_api_service.types import Rate


class RatesRepoABC:
    @abc.abstractmethod
    def get_rates(
        self,
        origin,
        destination,
        date_from,
        date_to,
    ) -> List[Rate]:
        """get average rates for route and date interval"""
