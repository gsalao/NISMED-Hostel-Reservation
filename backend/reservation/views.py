from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ReservationSerializer 
from .utils import are_dates_available
from guest.utils import insert_guest
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import Reservation

# Create your views here.
'''
possible views for reservation:
2. post a new reservation ✓ 
'''

@api_view(['POST'])
def create_new_reservation(request):
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

    if end_date <= start_date:
        return Response({"error": "End date cannot happen before the start"}, status=status.HTTP_400_BAD_REQUEST)

    # Room counts
    reserved_room_counts = {
        'A': request.data.get("single_a_room_count", 0) + request.data.get("double_a_room_count", 0),
        'B': request.data.get("single_b_room_count", 0) + request.data.get("double_b_room_count", 0),
        'C': request.data.get("single_c_room_count", 0) + request.data.get("double_c_room_count", 0) + request.data.get("triple_c_room_count", 0),
    }

    if not are_dates_available(start_date, end_date, reserved_room_counts):
        return Response({"error": "Dates not available"}, status=status.HTTP_400_BAD_REQUEST)

    verification_code = get_random_string(length=6, allowed_chars='0123456789')

    reservation_data = {
        "guest_id": guest.id,
        "start_date": start_date,
        "end_date": end_date,
        "for_person_name": request.data.get("for_person_name"),
        "by_person_name": guest_name,
        "male_count": request.data.get("male_count"),
        "female_count": request.data.get("female_count"),
        "single_a_room_count": request.data.get("single_a_room_count", 0),
        "double_a_room_count": request.data.get("double_a_room_count", 0),
        "single_b_room_count": request.data.get("single_b_room_count", 0),
        "double_b_room_count": request.data.get("double_b_room_count", 0),
        "single_c_room_count": request.data.get("single_c_room_count", 0),
        "double_c_room_count": request.data.get("double_c_room_count", 0),
        "triple_c_room_count": request.data.get("triple_c_room_count", 0),
        "verification_code": verification_code,
        "is_verified": False,
    }

    serializer = ReservationSerializer(data=reservation_data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    reservation = serializer.save()

    send_mail(
        subject="Reservation Verification Code",
        message=f"Thank you for your reservation.\n\nYour verification code is: {verification_code}",
        from_email="noreply@example.com",
        recipient_list=[guest_email],
        fail_silently=False,
    )

    return Response({ "reservation_id": reservation.id }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def verify_reservation(request):
    reservation_id = request.data.get("reservation_id")
    code = request.data.get("code")

    try:
        reservation = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        return Response({"error": "Reservation not found"}, status=status.HTTP_404_NOT_FOUND)

    if reservation.verification_code == code:
        reservation.is_verified = True
        reservation.save()

        send_mail(
            subject="New Verified Reservation",
            message=f"Reservation #{reservation.id} has been verified by {reservation.by_person_name}.",
            from_email="noreply@example.com",
            recipient_list=["admin@example.com"],  # Replace with actual admin
            fail_silently=True,
        )

        return Response({"success": True})
    else:
        return Response({"error": "Invalid verification code"}, status=status.HTTP_400_BAD_REQUEST)