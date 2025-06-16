from django.db import models

# Create your models here.
class Guest(models.Model):
    """
    Represents the guests of a hostel, specifically the one that **reserved** the reservation

    Attributes
    ----------
    email_address: CharField
        The email address of the guest 
    for_name: CharField
        The name of the entity the reservation is for
    by_name: CharField
        The name of the entity making the reservation
    phone_number: CharField
        The phone number of entity making the reservation
    address: CharField
        The address of the entity making the reservation
    """
    email_address = models.CharField(max_length=256, primary_key=True)
    for_person_name = models.CharField(max_length=1024)
    by_person_name = models.CharField(max_length=1024)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=1024)
