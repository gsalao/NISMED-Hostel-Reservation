from django.db import models

# TODO: status enum, no show, cancelled, checked in
# TODO: add foreign keys of guest and room type

# Create your models here.
class Reservation(models.Model):
    """
    Represents the reservations by a user

    Attributes
    ----------
    status: CharField
        The status of the reservation 
    reservation_date: DateTimeField
        The date when the reservation was set
    start_date: DateTimeField
        The date when the reservation will begin
    end_date: DateTimeField
        The date when the reservation will end 
    """
    status = models.CharField(max_length=10, default='') 
    reservation_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Reservation #{self.id} was reserved on {self.reservation_date} and will start on {self.start_date} and end on {self.end_date}"
