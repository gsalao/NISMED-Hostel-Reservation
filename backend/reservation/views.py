from django.shortcuts import render
from .models import Reservation, status_symbols, status_symbols_reverse 
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import ReservationSerializer 
from .utils import valid_reservation
from room.models import RoomType

# Create your views here.
'''
possible views for reservation:
1. get all reservations, given a status ✓
2. post a new reservation ✓ 
3. post a reservation as done, cancelled, etc. ✓
4. maybe one for changing the room type of a reservation?
'''

# TODO: add restriction to who can use this request
@api_view(['GET'])
def get_all_reservations_status(request):
    """
    Gets all the reservations given a status id.
    This assumes that the format of the request data would be:
    {
        'status': {integer between 1, ..., 4}
    }
    """
    id_of_status_reservations = status_symbols_reverse[request.data["status"]]
    status_reservations = Reservation.objects.filter(status=status_symbols[id_of_status_reservations].value) 
    serialized_status = ReservationSerializer(status_reservations, many=True)
    return Response(serialized_status.data)


@api_view(['POST'])
def create_new_reservation(request):
    """
    This corresponds to the post response of adding a new reservation
    This assumes that the request was done in format of:
    {
        guest_id = "...", 
        room_type_id = "...", 
        status = "..." (integer),
        reservation_date = "...", 
        start_date = "...",
        end_date = "...",
    }
    """
    data = request.data.copy()
    status_int = data["status"]
    data["status"] = status_symbols[status_int].value

    serializer = ReservationSerializer(data=data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Check if there are any available room types at the given dates 
    room_type_id = data.get("room_type_id")
    start_date = data.get("start_date")
    end_date = data.get("end_date")

    # Validate dates before serialization
    if not valid_reservation(room_type_id, start_date, end_date):
        return Response(
            {"detail": "No available rooms for the selected type and date range."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update the corresponding room_type_id's total reserved
    room_type = RoomType.objects.get(pk=room_type_id)
    room_type.total_reserved += 1
    room_type.save()

    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def change_reservation_status(request):
    """
    This corresponds to the post response of changing the reservation status 
    This assumes that the reqeust was done in format of:
    {
        reservation_id: "...",
        status = "..." (integer),
    }
    """
    reservation_id = request.data.get("reservation_id")
    status_id = request.data.get("status")
    new_status = status_symbols[status_id].value

    try:
        reservation = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        return Response({"error": "Reservation not found."},
                        status=status.HTTP_404_NOT_FOUND)

    reservation.status = new_status 
    reservation.save()

    serializer = ReservationSerializer(reservation)
    return Response(serializer.data, status=status.HTTP_200_OK)
