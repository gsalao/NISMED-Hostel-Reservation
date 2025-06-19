from reservation.models import Reservation
from room.models import Room, RoomType
from reservation.models import StatusEnum

def are_dates_available(start_date, end_date) -> bool:
    # get how many reservations overlap
    overlapping_reservations = Reservation.objects.filter(
        start_date__lt=end_date,
        end_date__gt=start_date,
        status=StatusEnum.CHECKED_IN.value,
    )

    # TODO: check if this works!
    type_a_availability = is_room_type_available('A', overlapping_reservations)
    type_b_availability = is_room_type_available('B', overlapping_reservations)
    type_c_availability = is_room_type_available('C', overlapping_reservations)

    return type_a_availability and type_b_availability and type_c_availability

def is_room_type_available(room_type_id, reservations) -> bool:
    """
    This function is responsible in determining if there are room types that are available within a range
    """

    room_type = RoomType.objects.get(pk=room_type_id)
    total_rooms = room_type.total_inventory
    rooms_reserved = 0
    
    # TODO: go through all the reservations and get the number of rooms reserved that are of that room type

    return rooms_reserved < total_rooms

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

