.\env\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata fixtures/guest.json
python manage.py loaddata fixtures/room_amenitys.json
python manage.py loaddata fixtures/room_type.json
python manage.py loaddata fixtures/room_room.json
python manage.py loaddata fixtures/room_rate.json
python manage.py loaddata fixtures/reservation_reservation.json
python manage.py loaddata fixtures/reservation_reservedrooms.json
python manage.py runserver
