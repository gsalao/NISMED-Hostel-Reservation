from django.db import models
from guest.models import Guest
from room.models import Room, RoomRate, RoomType
from enum import Enum
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.db.models import Q

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

class Capacity(Enum):
    SINGLE = 'Single'
    DOUBLE = 'Double'
    TRIPLE = 'Triple'

    @classmethod
    def choices(cls):
        return [(tag.value, tag.value) for tag in cls]


# Create your models here.
class Reservation(models.Model):
    """
    Represents the reservations by a user

    Attributes
    ----------
    guest: Guest
        The guest who did the reservation
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
    male_count: IntegerField
        Number of males in reservation
    female_count: IntegerField
        Number of females in reservation
    remarks: TextField
        Comments from the admin
    {occupancy}_{type}_room_count: IntegerField
        The number of inputted rooms to be reserved

    """
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    assigned_a_room = models.BooleanField(default=False)
    status = models.CharField(max_length=1024, choices=StatusEnum.choices(), default=StatusEnum.CHECKED_IN.value)
    reservation_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    for_person_name = models.CharField(max_length=1024)
    male_count = models.IntegerField()
    female_count = models.IntegerField()
    remarks = models.TextField(blank=True, null=True)

    # this is kinda bad ngl, you might wanna maintain s.t. this is NOT hardcoded (use ReservationRoomCount)
    # TODO: rewrite this part!
    single_a_room_count = models.IntegerField(default=0)
    double_a_room_count = models.IntegerField(default=0)
    single_b_room_count = models.IntegerField(default=0)
    double_b_room_count = models.IntegerField(default=0)
    single_c_room_count = models.IntegerField(default=0)
    double_c_room_count = models.IntegerField(default=0)
    triple_c_room_count = models.IntegerField(default=0)

    # For user email verification
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def clean(self):
        from .utils import are_dates_available
        # Validation: End date after start
        if self.end_date <= self.start_date:
            raise ValidationError("End date must be after start date.")

        # Validation: The end date CANNOT be more than two weeks from the start date
        if self.end_date > self.start_date + timedelta(weeks=2):
            raise ValidationError("End date must only be within 2 weeks from the start date")

        # Validation: room counts cannot be all zero
        if self.single_a_room_count == self.single_b_room_count == self.single_c_room_count == self.double_a_room_count == self.double_b_room_count == self.double_c_room_count == self.triple_c_room_count == 0:
            raise ValidationError("There must be 1 occupant in a room")

        valid_dates, total_counts = are_dates_available(self.start_date, self.end_date, self.get_room_counts(), self) 
        if not valid_dates and self.status == StatusEnum.CHECKED_IN.value: 
            raise ValidationError(f"The reservation cannot be made; {self.show_unavailable_rooms(total_counts)}")

    def get_room_counts(self):
        return {
            'A': self.single_a_room_count + self.double_a_room_count,
            'B': self.single_b_room_count + self.double_b_room_count,
            'C': self.single_c_room_count + self.double_c_room_count + self.triple_c_room_count
        }

    def show_unavailable_rooms(self, total_count):
        final_output = "You cannot reserve your listed amount of: "
        for (key,_) in total_count.items():
            final_output += f"{key} room/s"
        return final_output 

    def show_room_counts(self):
        rooms_counts = self.get_room_counts()
        final_output = ""
        if rooms_counts['A'] != 0: final_output += f"{rooms_counts['A']} A {'rooms' if rooms_counts['A'] > 1 else 'room'}"
        if rooms_counts['B'] != 0: final_output += f"{rooms_counts['B']} B {'rooms' if rooms_counts['B'] > 1 else 'room'}"
        if rooms_counts['C'] != 0: final_output += f"{rooms_counts['C']} C {'rooms' if rooms_counts['C'] > 1 else 'room'}"
        return final_output 

    def __str__(self):
        return f"Reservation #{self.id}: {self.show_room_counts()}"

class ReservedRoom(models.Model):
    """
    Represents the reserved room of a user
    """
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType , on_delete=models.CASCADE)
    capacity = models.CharField(max_length=1024, choices=Capacity.choices(), blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    room_rate = models.ForeignKey(RoomRate, on_delete=models.CASCADE)

    def clean(self):
        super().clean()

        # if the reservation is not checked in 
        if self.reservation.status != StatusEnum.CHECKED_IN.value:
            raise ValidationError("You cannot use this reservation")

        # if the reserved room has been selected
        overlapping_reservations = ReservedRoom.objects.filter(
            room=self.room
        ).exclude(pk=self.pk).filter(
            Q(reservation__start_date__lt=self.reservation.end_date) &
            Q(reservation__end_date__gt=self.reservation.start_date)
        )

        if overlapping_reservations.exists():
            raise ValidationError(f"Room '{self.room}' is already reserved during the selected period.")
    def __str__(self):
        return f"A reserved room for Reservation #{self.reservation.id}"
