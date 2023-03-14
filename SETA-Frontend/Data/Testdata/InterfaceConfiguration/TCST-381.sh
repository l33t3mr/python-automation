#!/bin/sh
set -e

# Check for the expected command.
PARAMS="$@"
if [ "$1" = 'uwsgi' ] || [ "${PARAMS#*manage.py}" != "$PARAMS" ]; then
	if [ "$MODE" != 'worker' ] && [ "$MODE" != 'testing' ]; then
        # Run collectstatic here, because we need SECRET_KEY and
        # DB_PASSWORD to run manage.py commands. So we can not
        # invoke it in the Dockerfile.
        python3 manage.py collectstatic --noinput
    fi
    # Wait for database
    RETRIES=30
    until pg_isready -h $DB_HOST -p $DB_PORT > /dev/null 2>&1 || [ $RETRIES -eq 0 ]; do
        echo "Waiting for postgres server, $((RETRIES-=1)) remaining attempts..."
        sleep 1
    done
    if [ "$MODE" != 'worker' ]; then
        # Apply migrations.
        python3 manage.py migrate --noinput
        # Create superuser if necessary.
        if [ -n "$SUPERUSER_USERNAME" ] && [ "$MODE" != 'testing' ]; then
            if [ -n "$SUPERUSER_INITIAL_PASSWORD" ]; then
                # Add superuser, if necessary
                cat <<EOF | python3 manage.py shell
from django.contrib.auth import get_user_model

User = get_user_model()

if User.objects.filter(username="$SUPERUSER_USERNAME").exists():
    print('Superuser already exists. Skipping creation...')
else:
    User.objects.create_superuser("$SUPERUSER_USERNAME", "$SUPERUSER_MAIL", "$SUPERUSER_INITIAL_PASSWORD")
    print('Successfully created superuser.')
EOF
            else
                echo "\$SUPERUSER_INITIAL_PASSWORD is empty. Abort..."
                exit 1
            fi
        fi
    fi
    # Start the Django Q Cluster, if the corresponding mode is given.
    if [ "$MODE" = 'worker' ]; then
        exec python3 manage.py qcluster
    elif [ "$MODE" = 'hybrid' ]; then
        python3 manage.py qcluster &
    fi
fi

# Run seta or whatever the user wanted like "bash" or "sh".
# Since we are not required to initiate stuff as root,
# we are already running as seta user and do not have 
# to drop privileges here.
exec "$@"
