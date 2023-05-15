#!/bin/sh
# entrypoint.sh

python manage.py migrate

# Switch to the main container `CMD`.
exec "$@"
