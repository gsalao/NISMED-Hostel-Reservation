#!/usr/bin/env bash
# Build script for Render deployments.
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate

# Seed the database with fixtures on the first deploy only, so reservations
# made on the live site are not clobbered by later deploys.
if python manage.py shell -c "from room.models import Room; import sys; sys.exit(0 if Room.objects.exists() else 1)"; then
    echo "Database already seeded; skipping fixtures."
else
    echo "Seeding database from fixtures..."
    python manage.py loaddata \
        fixtures/room_amenitys.json \
        fixtures/room_type.json \
        fixtures/room_room.json \
        fixtures/room_rate.json \
        fixtures/room_type_image.json \
        fixtures/guest.json \
        fixtures/reservation_reservation.json \
        fixtures/reservation_reservedrooms.json
fi

# Create the admin account if DJANGO_SUPERUSER_* env vars are set (free tier
# has no shell, so this is the only way to get a superuser).
if [ -n "${DJANGO_SUPERUSER_USERNAME:-}" ]; then
    python manage.py createsuperuser --noinput || true
fi
