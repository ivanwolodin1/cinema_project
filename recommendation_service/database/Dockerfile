FROM postgres:latest
WORKDIR /var/lib/postgres
COPY create_fixtures.sql /docker-entrypoint-initdb.d/create_fixtures.sql
