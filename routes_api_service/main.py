import logging

from waitress import serve

from routes_api_service.app import create_app
from routes_api_service.io.rates_repo_postgres.rates_repo_postgres import (
    RatesRepoPostgres,
)
from settings import Settings


def main():
    settings = Settings()
    repo = RatesRepoPostgres(
        settings.dbname,
        settings.dbuser,
        settings.dbpassword,
        settings.dbhost,
        settings.dbport,
    )
    with repo.connection():
        app = create_app(repo, settings.debug)
        if settings.debug:
            logging.info("starting dev service...")
            app.run(debug=settings.debug)
        else:
            logging.info("starting production service...")
            serve(app, host=settings.api_host, port=settings.api_port)


if __name__ == "__main__":
    main()
