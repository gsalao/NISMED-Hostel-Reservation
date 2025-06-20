from django.db import models

# Create your models here.
# TODO: maybe make the phone number more restrictive and consistent? idk tho
class Guest(models.Model):
    """
    Represents the guests of a hostel, specifically the one that **reserved** the reservation

    Attributes
    ----------
    email_address: CharField
        The email address of the guest 
    phone_number: CharField
        The phone number of entity making the reservation
    address: CharField
        The address of the entity making the reservation
    name: CharField
        The name of the entity making the reservation
    """
    email_address = models.CharField(max_length=256, unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=1024)
    name = models.CharField(max_length=2014)

    def __str__(self):
        return self.email_address
