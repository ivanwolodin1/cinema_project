#!/bin/sh
set -e

echo Starting postgres
until PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DB -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  echo $POSTGRES_USER
  echo $POSTGRES_PASSWORD
  sleep 1
done
echo PostgreSQL started

alembic upgrade head
echo DB table created

python init_data.py
echo Initial data inserted

nohup python main.py