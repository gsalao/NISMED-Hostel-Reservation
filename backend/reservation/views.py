from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ReservationSerializer 
from .utils import are_dates_available
from guest.utils import insert_guest
from django.core.exceptions import ValidationError
from django.core.mail import send_mail, BadHeaderError
from smtplib import SMTPException
from django.utils.crypto import get_random_string
from .models import Reservation

# Temporary store for unverified reservations (use cache/DB/session in production)
PENDING_VERIFICATIONS = {}

@api_view(['POST'])
def create_new_reservation(request):
    guest_email = request.data.get("guest_email")
    guest_name = request.data.get("guest_name")
    phone_number = request.data.get("phone_number")
    address = request.data.get("address")

    start_date = request.data.get("start_date")
    end_date = request.data.get("end_date")

    if end_date <= start_date:
        return Response({"error": "End date cannot be before the start date"}, status=status.HTTP_400_BAD_REQUEST)

    reserved_room_counts = {
        'A': request.data.get("single_a_room_count", 0) + request.data.get("double_a_room_count", 0),
        'B': request.data.get("single_b_room_count", 0) + request.data.get("double_b_room_count", 0),
        'C': request.data.get("single_c_room_count", 0) + request.data.get("double_c_room_count", 0) + request.data.get("triple_c_room_count", 0),
    }

    if not are_dates_available(start_date, end_date, reserved_room_counts):
        return Response({"error": "Dates not available"}, status=status.HTTP_400_BAD_REQUEST)

    verification_code = get_random_string(length=6, allowed_chars='0123456789')

    reservation_data = {
        "guest_email": guest_email,
        "guest_name": guest_name,
        "phone_number": phone_number,
        "address": address,
        "start_date": start_date,
        "end_date": end_date,
        "for_person_name": request.data.get("for_person_name"),
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

    temp_id = get_random_string(length=12)
    PENDING_VERIFICATIONS[temp_id] = reservation_data

    verification_link = f"http://localhost:5173/verify?token={temp_id}"

    try:
        send_mail(
            subject="UP NISMED Hostel - Verification Code",
            message=(
                f"Thank you for your reservation.\n\n"
                f"Please verify your reservation by clicking the link below:\n"
                f"{verification_link}\n\n"
                f"Or use this verification code: {verification_code}"
            ),
            from_email="noreply@up.edu.ph",
            recipient_list=[guest_email],
            fail_silently=False,
            html_message=f"""
                <p>Thank you for your reservation at UP NISMED Hostel, {guest_name}!</p>
                <p><strong>Start Date:</strong> {start_date}<br>
                <strong>End Date:</strong> {end_date}</p>
                <p>Please verify your reservation by clicking the link below:<br>
                <a href="{verification_link}">{verification_link}</a></p>
                <p>Your verification code is <u><strong>{verification_code}</strong></u></p>
            """
        )
        return Response({"reservation_token": temp_id}, status=status.HTTP_202_ACCEPTED)

    except (BadHeaderError, SMTPException) as e:
        return Response({"error": f"Failed to send email: {str(e)}"}, status=500)
    

@api_view(['POST'])
def verify_reservation(request):
    token = request.data.get("reservation_token")
    code = request.data.get("code")

    if token not in PENDING_VERIFICATIONS:
        return Response({"error": "Invalid or expired reservation token."}, status=status.HTTP_404_NOT_FOUND)

    reservation_data = PENDING_VERIFICATIONS[token]

    if reservation_data["verification_code"] != code:
        return Response({"error": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)

    # Create guest only after successful verification
    try:
        guest = insert_guest(
            reservation_data["guest_email"],
            reservation_data["guest_name"],
            reservation_data["phone_number"],
            reservation_data["address"]
        )
    except ValidationError as e:
        return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    serializer = ReservationSerializer(data={**reservation_data, "guest_id": guest.id})
    if serializer.is_valid():
        reservation = serializer.save(is_verified=True)

        try:
            send_mail(
                subject=f"NISMED Hostel Reservation - Reservation #{reservation.id}",
                message=f"Reservation #{reservation.id} verified.",
                from_email="noreply@up.edu.ph",
                recipient_list=["ghsalao@up.edu.ph"],
                fail_silently=True,
                html_message=f"""
                    <p><strong>Reservation #{reservation.id}</strong> has been verified.</p>
                    <p><strong>Start Date:</strong> {reservation.start_date}<br>
                    <strong>End Date:</strong> {reservation.end_date}</p>
                """
            )

            send_mail(
                subject=f"UP NISMED Hostel - Successful Reservation",
                message=f"Reservation #{reservation.id} has been verified.",
                from_email="noreply@up.edu.ph",
                recipient_list=[reservation_data["guest_email"]],
                fail_silently=True,
                html_message=f"""
                    <p>Congratulations! Your reservation has been verified.</p>
                    <p><strong>Start Date:</strong> {reservation.start_date}<br>
                    <strong>End Date:</strong> {reservation.end_date}</p>
                """
            )

            del PENDING_VERIFICATIONS[token]
            return Response({"success": True})

        except (BadHeaderError, SMTPException) as e:
            del PENDING_VERIFICATIONS[token]
            return Response({"error": f"Failed to send confirmation email: {str(e)}"}, status=500)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)