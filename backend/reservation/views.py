from django.shortcuts import render
from .models import Reservation, status_symbols, status_symbols_reverse 
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import ReservationSerializer 
from .utils import find_available_room, is_room_type_available

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
        guest_id = "...", should be an email address
        room_type_id = "...", 
        start_date = "...",
        end_date = "...",
    }
    """
    room_type_id = request.data.get("room_type_id")
    start_date = request.data.get("start_date")
    end_date = request.data.get("end_date")

    # Check if there are any available room types at the given dates 
    if not is_room_type_available(room_type_id, start_date, end_date):
        return Response({"error": "Room type not available"}, status=status.HTTP_400_BAD_REQUEST)

    # Check if there are any available rooms of that room type (just in case)
    if not (room := find_available_room(room_type_id, start_date, end_date)):
        return Response({"error": "No room found"}, status=status.HTTP_400_BAD_REQUEST)
    
    data = request.data.copy()
    data["room_id"] = room.id
    print(room.id)

    serializer = ReservationSerializer(data=data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
