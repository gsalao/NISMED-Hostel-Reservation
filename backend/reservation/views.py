from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ReservationSerializer 
from .utils import are_dates_available
from guest.utils import insert_guest
from django.core.exceptions import ValidationError
from datetime import timedelta

# Create your views here.
'''
possible views for reservation:
2. post a new reservation ✓ 
'''

@api_view(['POST'])
def create_new_reservation(request):
    """
    This corresponds to the post response of adding a new reservation
    This assumes that the request was done in format of:
    {
        "guest_name": "...",
        "guest_email": "...",
        "phone_number": "...",
        "address": "...",
        "start_date": "...",
        "end_date": "...",
        "for_person_name": "...",
        "male_count": "...",
        "female_count": "...",
        "single_a_room_count": "...", 
        "double_a_room_count": "...", 
        "single_b_room_count": "...", 
        "double_b_room_count": "...", 
        "single_c_room_count": "...", 
        "double_c_room_count": "...", 
        "triple_c_room_count": "...", 
    }
    """
    guest_email = request.data.get("guest_email")
    guest_name = request.data.get("guest_name")
    phone_number = request.data.get("phone_number")
    address = request.data.get("address")

    try:
        guest = insert_guest(guest_email, guest_name, phone_number, address)
    except ValidationError as e:
        return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
    
    start_date = request.data.get("start_date")
    end_date = request.data.get("end_date")
    single_a_room_count = request.data.get("single_a_room_count") 
    double_a_room_count = request.data.get("double_a_room_count") 
    single_b_room_count = request.data.get("single_b_room_count") 
    double_b_room_count = request.data.get("double_b_room_count") 
    single_c_room_count = request.data.get("single_c_room_count") 
    double_c_room_count = request.data.get("double_c_room_count") 
    triple_c_room_count = request.data.get("triple_c_room_count") 

    reserved_room_counts = {
        'A': single_a_room_count + double_a_room_count,
        'B': single_b_room_count + double_b_room_count,
        'C': single_c_room_count + double_c_room_count + triple_c_room_count
    }

    # Check if the end is after the start 
    if end_date <= start_date:
        return Response({"error": "End date cannot happen before the start"}, status=status.HTTP_400_BAD_REQUEST)

    if end_date > start_date + timedelta(weeks=2):
        raise ValidationError("End date cannot be more than two weeks after the start date.")

    # Check if there are any available room types at the given dates 
    if not are_dates_available(start_date, end_date, reserved_room_counts):
        return Response({"error": "Dates not available"}, status=status.HTTP_400_BAD_REQUEST)

    reservation_data = {
        "guest_id": guest.id,
        "start_date": start_date,
        "end_date": end_date,
        "for_person_name": request.data.get("for_person_name"),
        "by_person_name": request.data.get("by_person_name"),
        "male_count": request.data.get("male_count"),
        "female_count": request.data.get("female_count"),
        "single_a_room_count": single_a_room_count,
        "double_a_room_count": double_a_room_count,
        "single_b_room_count": single_b_room_count,
        "double_b_room_count": double_b_room_count,
        "single_c_room_count": single_c_room_count,
        "double_c_room_count": double_c_room_count,
        "triple_c_room_count": triple_c_room_count,
    }

    serializer = ReservationSerializer(data=reservation_data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

