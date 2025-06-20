from django.db import models
from guest.models import Guest
from room.models import Room, RoomRate
from enum import Enum
from django.core.exceptions import ValidationError

class StatusEnum(Enum):
    CHECKED_IN = 'CHECKED IN'
    NO_SHOW = 'NO SHOW' 
    CANCELLED = 'CANCELLED'
    CHECKED_OUT = 'CHECKED OUT' 

    @classmethod
    def choices(cls):
        return [(tag.value, tag.value) for tag in cls]

status_symbols = {
    1: StatusEnum.CHECKED_IN,
    2: StatusEnum.NO_SHOW,
    3: StatusEnum.CANCELLED,
    4: StatusEnum.CHECKED_OUT,
}

status_symbols_reverse = {
    StatusEnum.CHECKED_IN: 1,
    StatusEnum.NO_SHOW: 2,
    StatusEnum.CANCELLED: 3,
    StatusEnum.CHECKED_OUT: 4,
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
    for_name: CharField
        The name of the entity the reservation is for
    by_name: CharField
        The name of the entity making the reservation
    male_count: IntegerField
        Number of males in reservation
    female_count: IntegerField
        Number of females in reservation
    remarks: TextField
        Comments from the admin
    {occupancy}_{type}_room_count: IntegerField
        The number of inputted rooms to be reserved

    """
    guest_id = models.ForeignKey(Guest, on_delete=models.CASCADE)
    status = models.CharField(max_length=1024, choices=StatusEnum.choices(), default=StatusEnum.CHECKED_IN.value)
    reservation_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    for_person_name = models.CharField(max_length=1024)
    by_person_name = models.CharField(max_length=1024)
    male_count = models.IntegerField()
    female_count = models.IntegerField()
    remarks = models.TextField(blank=True, null=True)

    # this is kinda bad ngl, you might wanna maintain s.t. this is NOT hardcoded (use ReservationRoomCount)
    # TODO: rewrite this part!
    single_a_room_count = models.IntegerField()
    double_a_room_count = models.IntegerField()
    single_b_room_count = models.IntegerField()
    double_b_room_count = models.IntegerField()
    single_c_room_count = models.IntegerField()
    double_c_room_count = models.IntegerField()
    triple_c_room_count = models.IntegerField()

    def clean(self):
        from .utils import are_dates_available
        # Validation: Cannot start in the past
        # if self.start_date < timezone.now().date():
        #     raise ValidationError("Reservation cannot start in the past.")

        # Validation: End date after start
        if self.end_date <= self.start_date:
            raise ValidationError("End date must be after start date.")

        # Validation: room counts cannot be all zero
        if self.single_a_room_count == self.single_b_room_count == self.single_c_room_count == self.double_a_room_count == self.double_b_room_count == self.double_c_room_count == self.triple_c_room_count == 0:
            raise ValidationError("There must be 1 occupant in a room")

        # TODO: call the are_dates_available function in `utils.py`
        if not are_dates_available(self.start_date, self.end_date):
            raise ValidationError("The reservation cannot be made")

        # if overlapping.exists():
        #     raise ValidationError(f"Room {self.room_id} is not available for the selected dates.")

    def get_room_counts(self):
        return {
            'A': self.single_a_room_count + self.double_a_room_count,
            'B': self.single_b_room_count + self.double_b_room_count,
            'C': self.single_c_room_count + self.double_c_room_count + self.triple_c_room_count
        }

    def __str__(self):
        return f"Reservation was reserved on {self.reservation_date.date()} and will start on {self.start_date} and end on {self.end_date}"

class ReservedRoom(models.Model):
    """
    Represents the reserved room of a user
    """
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    room_rate = models.ForeignKey(RoomRate, on_delete=models.CASCADE)
    # room_count = models.IntegerField(default=1)

