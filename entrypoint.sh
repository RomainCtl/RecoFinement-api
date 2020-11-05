#!/bin/sh

echo "Waiting for postgres..."
while ! nc -z $DB_URL $DB_PORT; do
    sleep 1
done
echo "PostgreSQL started"

# Create database structure (or upgrade it)
pipenv run flask db upgrade

exec "$@"
