from waitress import serve

from routes_api_service.app import create_app
from routes_api_service.io.rates_repo_postgres.rates_repo_postgres import (
    RatesRepoPostgres,
)
from settings import Settings


def main():
    settings = Settings()
    repo = RatesRepoPostgres(
        settings.dbname, settings.user, settings.password, settings.host, settings.port
    )
    with repo.connection():
        app = create_app(repo, settings.debug)
        if settings.debug:
            app.run(debug=settings.debug)
        else:
            serve(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
