from django.db import models

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

    def __str__(self):
        return f"RoomType {self.name} (Available Rooms: {self.available_rooms})"

class RoomRate(models.Model):
    """
    The rate of a room (it will depend on the number of people)

    Attributes
    ----------
    room_type_id: RoomTypeId
        The room type that the rate is associated with
    occupancy: IntegerField
        The number of people that correspond to this rate
    rate: DecimalField 
        The rate of the room type given the occupancy per day
    """
    room_type_id = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='room_rates')
    occupancy = models.IntegerField() 
    rate = models.DecimalField(max_digits = 6, decimal_places = 2)

    def __str__(self):
        return f"Rate of a {self.room_type_id} with {self.occupancy} people: {self.rate} Php"

class Room(models.Model):
    """
    A room in the hostel

    Attributes
    ----------
    room_type_id: RoomTypeId
        The room type that the rate is associated with
    room_number: IntegerField
        The actual room number of the said room
    is_active: BooleanField
        If the room is available to be occupied
    """
    room_type_id = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Room #{self.room_number}: ({'Available' if self.is_active else 'Unavailable'})"
