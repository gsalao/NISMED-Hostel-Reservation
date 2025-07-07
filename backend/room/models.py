from django.db import models
from django.core.exceptions import ValidationError
from .storage import OverwriteStorage

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
    name = models.CharField(max_length=1, help_text="Name of the room type")
    available_rooms = models.IntegerField(help_text="The number of available rooms of that room type (Any changes in the number of rooms must be changed here)")
    amenities = models.ManyToManyField('Amenity', related_name='room_types', blank=True, help_text="The amenities of the room type")

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
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='room_rates', help_text="The room type of this room rate")
    occupancy = models.IntegerField(help_text="The amount of guests who occupy the room in accordance to the rate") 
    rate = models.DecimalField(max_digits = 9, decimal_places = 2, help_text="The rate according to the room type and the occupancy")

    def clean(self):
        """
        This method is mainly for validating that the inputted entries for the model is correct
        """
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
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='rooms', help_text="The type of room")
    room_number = models.IntegerField(help_text="The room number of the room")
    is_active = models.BooleanField(default=True, help_text="Check this if the room is available (i.e. uncheck this if the room is unavailable due to repairs and other concerns)")
    
    def clean(self):
        """
        This method is mainly for validating that the inputted entries for the model is correct
        """
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

class RoomTypeImage(models.Model):
    """
    This is the images of a room type
    """
    name = models.CharField(max_length=255, help_text="The name of the image")
    image = models.ImageField(upload_to='room_type_images/', storage=OverwriteStorage(), help_text="The image of the room type")
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, help_text="The room type of this image")

    def __str__(self):
      return f"{self.name}" 
