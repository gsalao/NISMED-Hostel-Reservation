from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import GuestSerializer 
from .models import Guest 

# Create your views here.
'''
possible views for guest:
1. get all guests
2. post a new guest if not present
'''

@api_view(['POST'])
def insert_guest(request):
    """
    This corresponds to the post response of adding a new guest, IF they haven't been added.
    This assumes that the request was done in format of:
    {
        "email_address": "...",
        "phone_number": "...",
        "address": "...",
    }
    """
    serializer = GuestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    email = serializer.validated_data.get('email_address')
    guest_exists = Guest.objects.filter(email_address=email).exists()

    if guest_exists:
        return Response({'detail': 'Guest email has been used'}, status=status.HTTP_409_CONFLICT)

    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

