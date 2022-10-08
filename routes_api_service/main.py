from routes_api_service.app import create_app
from routes_api_service.io.rates_repo_postgres.rates_repo_postgres import RatesRepoPostgres
from routes_api_service.settings import Settings

if __name__ == "__main__":
    settings = Settings()
    repo = RatesRepoPostgres(settings.dbname, settings.user, settings.password, settings.host, settings.port)
    with repo.connection():
        app = create_app(repo)
        app.run(debug=settings.debug)
