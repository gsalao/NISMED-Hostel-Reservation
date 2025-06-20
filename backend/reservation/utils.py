from .models import Reservation, ReservedRoom
from room.models import Room, RoomType
from reservation.models import StatusEnum
from django.db.models import Count

def are_dates_available(start_date, end_date) -> bool:
    # get how many reservations overlap
    overlapping_reservations = Reservation.objects.filter(
        start_date__lt=end_date,
        end_date__gt=start_date,
        status=StatusEnum.CHECKED_IN.value,
    )

    # get all reserved rooms on those reservations:
    reserved_rooms = ReservedRoom.objects.filter(reservation__in=overlapping_reservations)

    # group the reserved rooms by room type (i.e. grouping by room's room type foreign key) and it will count the number of entries
    reserved_by_type = (
        reserved_rooms
        .values('room__room_type')
        .annotate(total_reserved=Count('id'))
    )

    # Convert to a dict: {room_type_id: reserved_count}
    reserved_count_map = {entry['room__room_type']: entry['total_reserved'] for entry in reserved_by_type}

    # Compare against room type inventory
    for room_type in RoomType.objects.all():
        reserved = reserved_count_map.get(room_type.id, 0)
        if reserved >= room_type.total_inventory:
            return False  # Not enough rooms of this type

    return True


def find_available_room(room_type_id, start_date, end_date):
    """
    This function is responsible in determining if there are rooms of a certain room type that are available within a range - it basically assigns the first available room
    """
    rooms = Room.objects.filter(room_type_id=room_type_id)

    for room in rooms:
        overlap = Reservation.objects.filter(
            room_id=room,
            start_date__lt=end_date,
            end_date__gt=start_date,
            status=StatusEnum.CHECKED_IN.value,
            room_id__is_active=True
        ).exists()

        if not overlap:
            return room  # First available room

    return None  # No available rooms

