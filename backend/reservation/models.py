from django.db import models
from guest.models import Guest
from room.models import RoomType
from enum import Enum

class StatusEnum(Enum):
    NO_SHOW = 'No Show'
    CANCELLED = 'Cancelled'
    CHECKED_IN = 'Checked In'
    DONE = 'Done'

status_symbols = {
    1: StatusEnum.NO_SHOW,
    2: StatusEnum.CANCELLED,
    3: StatusEnum.CHECKED_IN,
    4: StatusEnum.DONE,
}

status_symbols_reverse = {
    StatusEnum.NO_SHOW: 1,
    StatusEnum.CANCELLED: 2,
    StatusEnum.CHECKED_IN: 3,
    StatusEnum.DONE: 4,
}

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
    guest_id = models.ForeignKey(Guest, on_delete=models.CASCADE)
    room_type_id = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, default=StatusEnum.CHECKED_IN)
    reservation_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Reservation #{self.id} was reserved on {self.reservation_date} and will start on {self.start_date} and end on {self.end_date}"
