from rest_framework import serializers
from .models import Room, RoomType, RoomRate 

class RoomSerializer(serializers.ModelSerializer):
    str = serializers.SerializerMethodField()
    class Meta:
        model = Room 
        fields = '__all__' 

    def get_str(self, obj):
        return str(obj)

class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType 
        fields = '__all__' 

class RoomRateSerializer(serializers.ModelSerializer):
    str = serializers.SerializerMethodField()
    class Meta:
        model = RoomRate 
        fields = '__all__' 
    def get_str(self, obj):
        return str(obj)

