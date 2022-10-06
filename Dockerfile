FROM  postgres:12
COPY rates.sql /docker-entrypoint-initdb.d/
COPY destinations.csv /destinations.csv
EXPOSE 5432
ENV POSTGRES_PASSWORD=ratestask
