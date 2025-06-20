from .serializers import GuestSerializer
from .models import Guest 

def insert_guest(email_address, name, phone_number, address):
    """
    This corresponds to the post response of adding a new guest, IF they haven't been added.
    This assumes that the request was done in format of:
    {
        "email_address": "...",
        "phone_number": "...",
        "address": "...",
        "name": "...",
    }
    """
    guest = Guest.objects.filter(email_address=email_address).first()
    if guest:
        return guest

    guest_data = {
        'email_address': email_address,
        'phone_number': phone_number, 
        'address': address, 
        'name': name, 
    }

    guest_serializer = GuestSerializer(data=guest_data)
    guest_serializer.is_valid(raise_exception=True)
    return guest_serializer.save()
