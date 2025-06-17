from rest_framework import serializers
from .models import Room, RoomType, RoomRate 

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room 
        fields = '__all__' 

class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType 
        fields = '__all__' 

class RoomRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomRate 
        fields = '__all__' 

