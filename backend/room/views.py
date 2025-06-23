from django.shortcuts import render
from .models import Room, RoomType, RoomRate 
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RoomSerializer, RoomTypeSerializer, RoomRateSerializer 
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

# Create your views here.

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

class RoomAPIView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer 
    # Filter by Room 
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['room_type_id']
    permission_classes = [IsAuthenticated]

class RoomRateAPIView(generics.ListAPIView):
    queryset = RoomRate.objects.all()
    serializer_class = RoomRateSerializer 
    # Filter by Room Rate
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['room_type_id']
    permission_classes = [IsAuthenticated]
