from reservation.models import Reservation
from room.models import Room, RoomType
from reservation.models import StatusEnum

def is_room_type_available(room_type_id, start_date, end_date):
    """
    This function is responsible in determining if there are room types that are available within a range
    """
    room_type = RoomType.objects.get(pk=room_type_id)
    total_rooms = room_type.total_inventory

    # Count how many reservations overlap
    overlapping_reservations = Reservation.objects.filter(
        room_id__room_type_id=room_type_id,
        start_date__lt=end_date,
        end_date__gt=start_date,
        status=StatusEnum.CHECKED_IN.value,
        room_id__is_available=True
    ).count()

    return overlapping_reservations < total_rooms

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
            room_id__is_available=True
        ).exists()

        if not overlap:
            return room  # First available room

    return None  # No available rooms

