#!/bin/sh

set -e

wait_for_db() {
    if [ -z "$DB_HOST" ] || [ -z "$DB_PORT" ]; then
        echo "No django database host or port, not waiting for db."
    else
        echo "Waiting for database"
        dockerize -wait tcp://"$DB_HOST":"$DB_PORT" -timeout 30s
    fi
}

wait_for_db

echo "Running migrations"
# Apply database migrations
python manage.py migrate

# Collect static files
echo "Running collectstatic"
python manage.py collectstatic --noinput

exec "$@"
