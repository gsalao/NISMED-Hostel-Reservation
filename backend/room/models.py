from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class RoomType(models.Model):
    """
    This represents the type of room that is present in the hostel

    Attributes
    ----------
    name: CharField
        The specific name of the room type ('A', 'B', 'C')
    available_rooms: IntegerField
        The total number of available rooms
    """
    name = models.CharField(max_length=1)
    available_rooms = models.IntegerField()
    amenities = models.ManyToManyField('Amenity', related_name='room_types', blank=True)

    def __str__(self):
        return f"{self.name}" 

class RoomRate(models.Model):
    """
    The rate of a room (it will depend on the number of people)

    Attributes
    ----------
    room_type: RoomTypeId
        The room type that the rate is associated with
    occupancy: IntegerField
        The number of people that correspond to this rate
    rate: DecimalField 
        The rate of the room type given the occupancy per day
    """
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='room_rates')
    occupancy = models.IntegerField() 
    rate = models.DecimalField(max_digits = 9, decimal_places = 2)

    def clean(self):
        super().clean()
        if RoomRate.objects.filter(
            room_type=self.room_type,
            occupancy=self.occupancy
        ).exclude(pk=self.pk).exists():
            raise ValidationError("A rate with this room type and occupancy already exists.")

    def __str__(self):
        return f"{self.room_type} room {self.occupancy} pax: ₱{self.rate}"

class Room(models.Model):
    """
    A room in the hostel

    Attributes
    ----------
    room_type: RoomTypeId
        The room type that the rate is associated with
    room_number: IntegerField
        The actual room number of the said room
    is_active: BooleanField
        If the room is available to be occupied
    """
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    def clean(self):
        super().clean()
        if Room.objects.filter(
            room_number=self.room_number,
        ).exclude(pk=self.pk).exists():
            raise ValidationError("A room with this room number already exists.")

    def __str__(self):
        return f"Room #{self.room_number}"
    

class Amenity(models.Model):
    """
    This represents the amenities present per room in the hostel

    Attributes
    ----------
    name: CharField
        The name of the specific, available amenity
    """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
      return f"{self.name}" 

    class Meta:
        verbose_name_plural = 'Amenities'
