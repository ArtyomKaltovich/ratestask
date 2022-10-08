import logging

from flask import Flask, request
from pydantic import ValidationError

from routes_api_service.const import RATES_URL
from routes_api_service.io.rates_repo_abc import RatesRepoABC
from routes_api_service.models.request_args import RequestArgs


def create_app(rates_repo: RatesRepoABC, reraise_error):
    app = Flask(__name__)

    @app.get("/")
    def index():
        return "Rates API service started"

    @app.get(RATES_URL)
    def rates():
        try:
            args = RequestArgs(**request.args)
            return rates_repo.get_rates(
                args.origin, args.destination, args.date_from, args.date_to
            )
        except ValidationError as e:
            logging.warning(f"Invalid api request {e.raw_errors}")
            return e.json(), 400
        except Exception:
            logging.exception("Unexpected exception")
            if reraise_error:
                raise

    return app
