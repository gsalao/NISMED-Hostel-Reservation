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
    name = models.CharField(max_length=1024, help_text="The name of the guest")
    email_address = models.CharField(max_length=256, unique=True, help_text="The email address of the guest")
    phone_number = models.CharField(max_length=15, help_text="The phone number of the guest")
    address = models.CharField(max_length=1024, help_text="The address of the guest")

    def __str__(self):
        return self.email_address
