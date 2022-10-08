from contextlib import contextmanager
from functools import lru_cache
from pathlib import Path
from typing import List

import psycopg2

from routes_api_service.io.rates_repo_abc import RatesRepoABC
from routes_api_service.types import Rate


QUERIES_DIR = Path(__file__).parent / "sql"
RATES_QUERY = (QUERIES_DIR / "rates_query.sql").read_text()
RATES_QUERY_PLAN_NAME = "rates_query_plan"


class RatesRepoPostgres(RatesRepoABC):
    def __init__(
        self, dbname: str, user: str, password: str, host: str, port: int = 5432
    ):
        self._dbname = dbname
        self._user = user
        self._password = password
        self._host = host
        self._port = port
        self._conn = None

    @contextmanager
    def connection(self):
        self._conn = psycopg2.connect(
            dbname=self._dbname,
            user=self._user,
            password=self._password,
            host=self._host,
            port=self._port,
        )
        try:
            cur = self._conn.cursor()
            cur.execute(f"prepare {RATES_QUERY_PLAN_NAME} as {RATES_QUERY}")
            yield
        finally:
            self._conn.close()

    @lru_cache(10000)
    def get_rates(
        self,
        origin,
        destination,
        date_from,
        date_to,
    ) -> List[Rate]:
        """get average rates for route and date interval
        Usage
        -----
        repo = RatesRepoPostgres(...)
        with repo.connection():
            repo.get_rates(...)
        """
        try:
            cur = self._conn.cursor()  # type: ignore [attr-defined] # error: "None" has no attribute "cursor"
            cur.execute(
                f"execute {RATES_QUERY_PLAN_NAME} "
                f"('*.{origin}.*', '*.{destination}.*', '{date_from}', '{date_to}')"
            )
            return [Rate(day=r[0], average_price=r[1]) for r in cur]
        except AttributeError:
            raise TypeError(
                "Connection to db doesn't exist. "
                "Please execute this method inside inside connection context manager"
            )
