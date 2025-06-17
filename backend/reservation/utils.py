from reservation.models import Reservation
from room.models import Room, RoomType
from reservation.models import StatusEnum

from datetime import date

def is_room_type_available(room_type_id, start_date, end_date):
    room_type = RoomType.objects.get(pk=room_type_id)
    total_rooms = room_type.total_inventory

    # Count how many reservations overlap
    overlapping_reservations = Reservation.objects.filter(
        room_id__room_type_id=room_type_id,
        start_date__lt=end_date,
        end_date__gt=start_date,
        status=StatusEnum.CHECKED_IN.value
    ).count()

    print(Reservation.objects.filter(room_id__room_type_id=room_type_id,start_date__lt=end_date,end_date__gt=start_date,status=StatusEnum.CHECKED_IN.value))

    print(overlapping_reservations)
    print(total_rooms)

    return overlapping_reservations < total_rooms

def find_available_room(room_type_id, start_date, end_date):
    rooms = Room.objects.filter(room_type_id=room_type_id)

    for room in rooms:
        overlap = Reservation.objects.filter(
            room_id=room,
            start_date__lt=end_date,
            end_date__gt=start_date
        ).exists()

        if not overlap:
            return room  # First available room

    return None  # No available rooms

