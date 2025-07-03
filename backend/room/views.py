from django.shortcuts import render
from .models import Room, RoomType, RoomRate 
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RoomSerializer, RoomTypeSerializer, RoomRateSerializer 
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from reservation.models import Reservation, ReservedRoom

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
    """
    this class is primarily for filtering the dropdown menu for the admin panel; It filters the room based on the room type
    """
    serializer_class = RoomSerializer 
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['room_type_id']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This method is primarily for showing the possible room that you can select that will be shown in the dropdown menu given the inputted room type
        """
        queryset = Room.objects.filter(is_active=True)

        room_type = self.request.query_params.get('room_type_id')
        reservation = self.request.query_params.get('reservation')

        if room_type:
            queryset = queryset.filter(room_type=room_type)

        if reservation:
            reservation = Reservation.objects.get(pk=reservation)
            start_date = reservation.start_date
            end_date = reservation.end_date

            # Get rooms reserved for overlapping periods
            overlapping_reserved_rooms = ReservedRoom.objects.filter(
                reservation__start_date__lt=end_date,
                reservation__end_date__gt=start_date
            ).exclude(reservation=reservation).values_list('room', flat=True)

            # Exclude these rooms
            queryset = queryset.exclude(id__in=overlapping_reserved_rooms)

        return queryset

class RoomRateAPIView(generics.ListAPIView):
    # Filter by Room Rate
    queryset = RoomRate.objects.all()
    serializer_class = RoomRateSerializer 
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['room_type_id']
    permission_classes = [IsAuthenticated]
