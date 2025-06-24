from .models import Reservation
from room.models import Room, RoomType
from reservation.models import StatusEnum
from django.db.models import Sum 

def are_dates_available(start_date, end_date, requested_counts, current_reservation=None) -> bool:

    # get how many reservations overlap
    overlapping_reservations = Reservation.objects.filter(
        start_date__lt=end_date,
        end_date__gt=start_date,
        status=StatusEnum.CHECKED_IN.value,
    )

    # it will count itself, so just remove itself from the overlapping_reservations count
    if current_reservation and current_reservation.pk:
        overlapping_reservations = overlapping_reservations.exclude(pk=current_reservation.pk)

    # print(overlapping_reservations)

    # Aggregate room counts for each type from all overlapping reservations
    aggregate = overlapping_reservations.aggregate(
        total_a=Sum('single_a_room_count') + Sum('double_a_room_count'),
        total_b=Sum('single_b_room_count') + Sum('double_b_room_count'),
        total_c=Sum('single_c_room_count') + Sum('double_c_room_count') + Sum('triple_c_room_count'),
    )

    current_counts = {
        'A': aggregate['total_a'] or 0,
        'B': aggregate['total_b'] or 0,
        'C': aggregate['total_c'] or 0,
    }

    # Compare against room type inventory
    for room_type in RoomType.objects.all():
        existing = current_counts.get(room_type.name, 0)
        requested = requested_counts.get(room_type.name, 0) 

        # print(f"{room_type.name}\nExisting: {existing}\nRequested: {requested}")

        if existing + requested > room_type.available_rooms:
            return False 

    return True
