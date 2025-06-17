from reservation.models import Reservation
from room.models import RoomType

from datetime import date

def valid_reservation(room_type_id, start_date, end_date):
    """
    Checks if there is an available room of the given RoomType between start_date and end_date.

    Returns True if there is at least 1 available room; False otherwise.
    """
    # Fetch the room type and its total inventory
    room_type = RoomType.objects.get(pk=room_type_id)
    total_inventory = room_type.total_inventory

    # CASE 1:
    # Existing reservation starts before or at requested start,
    # and ends after the requested start.
    case_1 = Reservation.objects.filter(
        room_type_id=room_type_id,
        start_date__lte=start_date,
        end_date__gt=start_date
    ).count()

    # CASE 2:
    # Existing reservation starts before or at requested end,
    # and ends after the requested end.
    case_2 = Reservation.objects.filter(
        room_type_id=room_type_id,
        start_date__lt=end_date,
        end_date__gte=end_date
    ).count()

    # CASE 3:
    # Existing reservation starts within the requested period
    # and ends within the requested period.
    case_3 = Reservation.objects.filter(
        room_type_id=room_type_id,
        start_date__gte=start_date,
        end_date__lte=end_date
    ).count()

    total_conflicts = case_1 + case_2 + case_3

    available_rooms = total_inventory - total_conflicts 
    return available_rooms > 0
