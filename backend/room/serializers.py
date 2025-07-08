from rest_framework import serializers
from .models import Room, RoomType, RoomRate, Amenity, RoomTypeImage

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['id', 'name']

class RoomSerializer(serializers.ModelSerializer):
    str = serializers.SerializerMethodField()
    class Meta:
        model = Room 
        fields = '__all__' 

    def get_str(self, obj):
        return str(obj)

class RoomTypeSerializer(serializers.ModelSerializer):
    amenities = AmenitySerializer(many=True, read_only=True)
    available_rooms = serializers.IntegerField(read_only=True)

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

class RoomTypeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomTypeImage
        fields = ['id', 'name', 'image', 'room_type']
