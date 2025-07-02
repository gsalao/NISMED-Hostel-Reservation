from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ReservationSerializer 
from .utils import are_dates_available
from guest.utils import insert_guest
from django.core.exceptions import ValidationError
from datetime import timedelta, datetime
from django.core.mail import send_mail, BadHeaderError
from smtplib import SMTPException
from django.utils.crypto import get_random_string
import decouple
from django.core.cache import cache
from room.models import RoomRate

def show_unavailable_rooms(total_count):
    final_output = "You cannot reserve your listed amount of: "
    for (key,_) in total_count.items():
        final_output += f"{key} room/s"
    return final_output 

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
        "verification_code": "...",
        "is_verified": "...",
        "guest_details": "...",
    }
    """

    guest_email = request.data.get("guest_email")
    guest_name = request.data.get("guest_name")
    phone_number = request.data.get("phone_number")
    address = request.data.get("address")

    start_date = request.data.get("start_date")
    end_date = request.data.get("end_date")

    single_a_room_count = request.data.get("single_a_room_count")
    double_a_room_count = request.data.get("double_a_room_count") 
    single_b_room_count = request.data.get("single_b_room_count") 
    double_b_room_count = request.data.get("double_b_room_count") 
    single_c_room_count = request.data.get("single_c_room_count") 
    double_c_room_count = request.data.get("double_c_room_count") 
    triple_c_room_count = request.data.get("triple_c_room_count") 

    guest_details = request.data.get("guest_details", "")

    reserved_room_counts = {
        'A': single_a_room_count + double_a_room_count,
        'B': single_b_room_count + double_b_room_count,
        'C': single_c_room_count + double_c_room_count + triple_c_room_count,
    }

    # Check if the end is after the start 
    if end_date <= start_date:
        return Response({"error": "End date cannot happen before the start"}, status=status.HTTP_400_BAD_REQUEST)

    if datetime.strptime(end_date, "%Y-%m-%d").date() > datetime.strptime(start_date, "%Y-%m-%d").date() + timedelta(weeks=2):
        return Response({"error" : "End date cannot be more than two weeks after the start date."}, status=status.HTTP_400_BAD_REQUEST)

    # Check if there are any available room types at the given dates 
    valid_dates, total_counts = are_dates_available(start_date, end_date, reserved_room_counts)
    if not valid_dates: 
        return Response({"error": f"Dates not available; {show_unavailable_rooms(total_counts)}"}, status=status.HTTP_400_BAD_REQUEST)

    verification_code = get_random_string(length=6, allowed_chars='0123456789')

    reservation_data = {
        "guest_email": guest_email,
        "guest_name": guest_name,
        "phone_number": phone_number,
        "address": address,
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
        "verification_code": verification_code,
        "is_verified": False,
        "guest_details": guest_details,
    }

    temp_id = get_random_string(length=12)

    # verification_code expiration set to 300 seconds == 5 minutes
    cache.set(f"reservation:{temp_id}", reservation_data, timeout=300)

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

    reservation_data = cache.get(f"reservation:{token}")

    if not reservation_data:
        return Response({"error": "Invalid or expired reservation token."}, status=status.HTTP_404_NOT_FOUND)

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

    try:
        start_date = datetime.strptime(reservation_data["start_date"], "%Y-%m-%d")
        end_date = datetime.strptime(reservation_data["end_date"], "%Y-%m-%d")
    except (ValueError, TypeError) as e:
        return Response({"error": f"Invalid date format in reservation data: {str(e)}"}, status=400)


    serializer = ReservationSerializer(data={**reservation_data, "guest": guest.id})
    if serializer.is_valid():
        reservation = serializer.save(is_verified=True)

        try:
            nights = (end_date - start_date).days

            start_date_str = start_date.strftime("%B %d, %Y")
            end_date_str = end_date.strftime("%B %d, %Y")

            # Preload all room rates into a dictionary to avoid multiple DB hits
            rate_lookup = {
                (rate.room_type.id, rate.occupancy): rate.rate
                for rate in RoomRate.objects.select_related('room_type')
            }

            # Room config with labels and rates
            room_configs = {
                "single_a_room_count": {"label": "Type A Single Occupancy (1 pax)", "rate": rate_lookup.get((3, 1), 0)},
                "double_a_room_count": {"label": "Type A Double Occupancy (2 pax)", "rate": rate_lookup.get((3, 2), 0)},
                "single_b_room_count": {"label": "Type B Single Occupancy (1 pax)", "rate": rate_lookup.get((2, 1), 0)},
                "double_b_room_count": {"label": "Type B Double Occupancy (2 pax)", "rate": rate_lookup.get((2, 2), 0)},
                "single_c_room_count": {"label": "Type C Single Occupancy (1 pax)", "rate": rate_lookup.get((1, 1), 0)},
                "double_c_room_count": {"label": "Type C Double Occupancy (2 pax)", "rate": rate_lookup.get((1, 2), 0)},
                "triple_c_room_count": {"label": "Type C Triple Occupancy (3 pax)", "rate": rate_lookup.get((1, 3), 0)},
            }

            # Calculate the total standing balance and initialize HTML Table Row container
            total_balance: int = 0
            total_balance_html: str = ""

            room_tables = ""
            for key, config in room_configs.items():
                count = getattr(reservation, key)
                if count > 0:
                    total = config["rate"] * count * nights
                    total_balance += total
                    room_tables += f"""
                        <table style="border-collapse: collapse; width: 100%; font-size: 14px; margin-bottom: 20px;">
                          <tr>
                            <th colspan="2" style="border: 1px solid #000; padding: 8px; background-color: #f0f0f0;">
                              {config["label"]}
                            </th>
                          </tr>
                          <tr>
                            <td style="border: 1px solid #000; padding: 8px;">Check-in Date (2PM)</td>
                            <td style="border: 1px solid #000; padding: 8px;">{start_date_str}</td>
                          </tr>
                          <tr>
                            <td style="border: 1px solid #000; padding: 8px;">Check-out Date (12NN)</td>
                            <td style="border: 1px solid #000; padding: 8px;">{end_date_str}</td>
                          </tr>
                          <tr>
                            <td style="border: 1px solid #000; padding: 8px;">No. of Nights</td>
                            <td style="border: 1px solid #000; padding: 8px;">{nights}</td>
                          </tr>
                          <tr>
                            <td style="border: 1px solid #000; padding: 8px;">Room Type</td>
                            <td style="border: 1px solid #000; padding: 8px;">{config["label"]}</td>
                          </tr>
                          <tr>
                            <td style="border: 1px solid #000; padding: 8px;">No. of Rooms</td>
                            <td style="border: 1px solid #000; padding: 8px;">{count}</td>
                          </tr>
                          <tr>
                            <td style="border: 1px solid #000; padding: 8px;">Rate (per night, Php)</td>
                            <td style="border: 1px solid #000; padding: 8px;">₱{config["rate"]:,.2f}</td>
                          </tr>
                          <tr>
                            <td style="border: 1px solid #000; padding: 8px;">Total Amount to be paid (Php)</td>
                            <td style="border: 1px solid #000; padding: 8px;"><strong>₱{total:,.2f}</strong></td>
                          </tr>
                        </table>
                    """

            total_balance_html = f"""
              <table style="border-collapse: collapse; width: 100%; font-size: 14px; margin-bottom: 20px;">
                <tr>
                  <td style="width: 50%; border: 1px solid #000; padding: 8px; background-color: #f0f0f0;">
                    <strong>
                      Total Outstanding Balance
                    </strong>
                  </td>
                  <td style="width: 50%; border: 1px solid #000; padding: 8px;">
                    <strong>
                      ₱{total_balance:,.2f}
                    </strong>
                  </td>
                </tr>
              </table>
            """

            html_client_message = f"""
                <p>Dear Mx. {reservation_data["guest_name"]},</p>
                <p>Thank you for choosing UP NISMED Hostel. Please see the details of your reservation below.</p>
                <br>
                {room_tables}
                {total_balance_html}
                <p>Also, please see the attached file for our house rules and a few reminders below:</p>
                <ul>
                  <li>Check-in time is 2PM, Check-out is 12NN.</li>
                  <li>Curfew hours: 11PM–5AM</li>
                  <li><strong>Any changes in reservation should be made 48 hours in advance.</strong></li>
                  <li>Present your ID card when you check in.</li>
                  <li>Payment can be made during your stay, and we only accept payment in cash.</li>
                </ul>
            """

            html_admin_message = f"""
              <p><strong>Reservation #{reservation.id}</strong> from {reservation_data["guest_name"]} has been verified.</p>
              <br>
              {room_tables}
              {total_balance_html}
            """

            # Send admin confirmation
            send_mail(
                subject=f"NISMED Hostel Reservation - Reservation #{reservation.id}",
                message=f"Reservation #{reservation.id} verified.",
                from_email="noreply@up.edu.ph",
                recipient_list=[decouple.config('EMAIL_HOST_USER')],
                fail_silently=True,
                html_message=html_admin_message
            )

            # Send guest confirmation
            send_mail(
                subject="UP NISMED Hostel - Successful Reservation",
                message=f"Reservation #{reservation.id} has been verified.",
                from_email="noreply@up.edu.ph",
                recipient_list=[reservation_data["guest_email"]],
                fail_silently=True,
                html_message=html_client_message
            )

            cache.delete(f"reservation:{token}")
            return Response({"success": True})

        except (BadHeaderError, SMTPException) as e:
            cache.delete(f"reservation:{token}")
            return Response({"error": f"Failed to send confirmation email: {str(e)}"}, status=500)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_reservation_email(request):
    token = request.GET.get('token')

    reservation_data = cache.get(f"reservation:{token}")

    if not reservation_data:
        return Response({"error": "Invalid or expired reservation token."}, status=status.HTTP_404_NOT_FOUND)

    return Response({ "email" : reservation_data["guest_email"] }, status=status.HTTP_200_OK)
