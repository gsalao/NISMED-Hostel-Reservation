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

# i feel like this could have been encapsulated into the same function, but im too lazy to think of how
@api_view(['POST'])
def create_new_room_type(request):
    """
    This corresponds to the post response of adding a new room type 
    This assumes that the request was done in format of:
    {
        "name": "...", # only one character allowed
        "total_inventory": "...",
        "total_reserved": "..."
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
        "room_type_id": "...",
        "room_number": "...", -> Add a check of the room number!
        also add a check for how many has been added!
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
        "room_type_id": "...",
        "occupancy": "...",
        "rate": "...",
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
    This corresponds to the post response of changing the inventory 
    This assumes that the reqeust was done in format of:
    {
        "room_type_id": "...",
        "new_inventory": "..."
    }
    """
    room_type_id = request.data.get("room_type_id")
    new_inventory = request.data.get("new_inventory")

    try:
        room_type = RoomType.objects.get(id=room_type_id)
    except RoomType.DoesNotExist:
        return Response({"error": "Room Type not found."},
                        status=status.HTTP_404_NOT_FOUND)

    room_type.total_inventory = new_inventory 
    room_type.save()

    serializer = RoomTypeSerializer(room_type)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def change_room_rate(request):
    """
    This corresponds to the post response of changing the room rate 
    This assumes that the reqeust was done in format of:
    {
        "room_type_id": "...",
        "occupancy": "...",
        "new_rate": "..."
        add the occupancy!
    }
    """
    room_type_id = request.data.get("room_type_id")
    new_rate = request.data.get("new_rate")
    occupancy = request.data.get("occupancy")

    try:
        room_rate = RoomRate.objects.get(room_type_id=room_type_id, occupancy=occupancy)
    except RoomRate.DoesNotExist:
        return Response({"error": "Room Rate not found."},
                        status=status.HTTP_404_NOT_FOUND)

    room_rate.rate = new_rate 
    room_rate.save()

    serializer = RoomRateSerializer(room_rate)
    return Response(serializer.data, status=status.HTTP_200_OK)

