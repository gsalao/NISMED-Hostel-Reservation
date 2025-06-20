from django.shortcuts import render
from .models import Room, RoomType, RoomRate 
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import RoomSerializer, RoomTypeSerializer, RoomRateSerializer 

# Create your views here.
'''
possible views for room:
1. post a new room ✓
2. post a new room type ✓
3. post a new room rate ✓
4. post to renew a room rate ✓
5. post to renew the room types inventory ✓
'''

@api_view(['GET'])
def get_all_rooms(request):
    """
    Gets all the rooms.
    """
    all_rooms = Room.objects.all() 
    serialized_rooms = RoomSerializer(all_rooms, many=True)
    return Response(serialized_rooms.data)

@api_view(['GET'])
def get_all_room_types(request):
    """
    Gets all the room types.
    """
    all_room_types = RoomType.objects.all() 
    serialized_room_types = RoomTypeSerializer(all_room_types, many=True)
    return Response(serialized_room_types.data)

@api_view(['GET'])
def get_all_room_rates(request):
    """
    Gets all the room rates.
    """
    all_room_rates = RoomRate.objects.all() 
    serialized_room_rates = RoomRateSerializer(all_room_rates, many=True)
    return Response(serialized_room_rates.data)

