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
6. post to renew the room's is_available
'''

# i feel like this could have been encapsulated into the same function, but im too lazy to think of how
@api_view(['POST'])
def create_new_room_type(request):
    """
    This corresponds to the post response of adding a new room type 
    This assumes that the request was done in format of:
    {
        name: "...", # only one character allowed
        total_inventory: "...",
        total_reserved: "..."
    }
    """
    serializer = RoomTypeSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # TODO: possibly add more checks here
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def create_new_room(request):
    """
    This corresponds to the post response of adding a new room type 
    This assumes that the request was done in format of:
    {
        room_type_id: "...",
        room_number: "...",
    }
    """
    serializer = RoomSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # TODO: possibly add more checks here
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def create_new_room_rate(request):
    """
    This corresponds to the post response of adding a new room type 
    This assumes that the request was done in format of:
    {
        room_type_id: "...",
        occupany: "...",
        rate: "...",
    }
    """
    serializer = RoomRateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # TODO: possibly add more checks here
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def change_room_type_inventory(request):
    """
    This corresponds to the post response of changing the reservation status 
    This assumes that the reqeust was done in format of:
    {
        room_type_id: "...",
        new_inventory: "..."
    }
    """
    room_type_id = request.data.get("room_type_id")
    new_inventory = request.data.get("new_inventory")

    try:
        room_type = RoomType.objects.get(id=room_type_id)
    except RoomType.DoesNotExist:
        return Response({"error": "Room Type not found."},
                        status=status.HTTP_404_NOT_FOUND)

    room_type.inventory = new_inventory 
    room_type.save()

    serializer = RoomTypeSerializer(room_type)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def change_room_rate(request):
    """
    This corresponds to the post response of changing the reservation status 
    This assumes that the reqeust was done in format of:
    {
        room_rate_id: "...",
        new_rate: "..."
    }
    """
    room_rate_id = request.data.get("room_rate_id")
    new_rate = request.data.get("new_rate")

    try:
        room_rate = RoomRate.objects.get(id=room_rate_id)
    except RoomRate.DoesNotExist:
        return Response({"error": "Room Type not found."},
                        status=status.HTTP_404_NOT_FOUND)

    room_rate.inventory = new_rate 
    room_rate.save()

    serializer = RoomRateSerializer(room_rate)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def change_room_availability(request):
    """
    This corresponds to the post response of changing the reservation status 
    This assumes that the reqeust was done in format of:
    {
        room_id: "...",
        new_availability: "..."
    }
    """
    room_id = request.data.get("room_id")
    new_availability = request.data.get("new_availability")

    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        return Response({"error": "Room Type not found."},
                        status=status.HTTP_404_NOT_FOUND)

    room.inventory = new_availability 
    room.save()

    serializer = RoomSerializer(room)
    return Response(serializer.data, status=status.HTTP_200_OK)

