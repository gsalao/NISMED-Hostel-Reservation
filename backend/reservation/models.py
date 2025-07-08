from django.db import models
from guest.models import Guest
from room.models import Room, RoomRate, RoomType
from enum import Enum
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.db.models import Q

class StatusEnum(Enum):
    """
    This enum is for showing the 'states' that a reservation can take
    """
    RESERVED = 'RESERVED'
    CHECKED_IN = 'CHECKED IN'
    NO_SHOW = 'NO SHOW' 
    CANCELLED = 'CANCELLED'
    CHECKED_OUT = 'CHECKED OUT' 

    @classmethod
    def choices(cls):
        return [(tag.value, tag.value) for tag in cls]

status_symbols = {
    0: StatusEnum.RESERVED,
    1: StatusEnum.CHECKED_IN,
    2: StatusEnum.NO_SHOW,
    3: StatusEnum.CANCELLED,
    4: StatusEnum.CHECKED_OUT,
}

class Capacity(Enum):
    """
    This enum is for representing the 'occupancy' associated with a reserved room
    """
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
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, help_text="Email of the guest who registered the reservation")
    assigned_a_room = models.BooleanField(default=False, help_text="Check this if the reservation has already been assigned room/s")
    status = models.CharField(max_length=1024, choices=StatusEnum.choices(), default=StatusEnum.RESERVED.value, help_text="The current status of the resevation")
    reservation_date = models.DateTimeField(auto_now_add=True, help_text="The date when the reservation was reserved")
    start_date = models.DateField(help_text="The check-in date of the reservation")
    end_date = models.DateField(help_text="The check-out date of the reservation")
    for_person_name = models.CharField(max_length=1024, help_text="To whom the reservation is for")
    male_count = models.IntegerField(help_text="Number of male guests")
    female_count = models.IntegerField(help_text="Number of female guests")
    remarks = models.TextField(blank=True, null=True, help_text="Remarks regarding the reservation")

    # this is kinda bad ngl, you might wanna maintain s.t. this is NOT hardcoded (use ReservationRoomCount)
    # TODO: rewrite this part!
    single_a_room_count = models.IntegerField(default=0, help_text="Number of A single rooms reserved")
    double_a_room_count = models.IntegerField(default=0, help_text="Number of A double rooms reserved")
    single_b_room_count = models.IntegerField(default=0, help_text="Number of B single rooms reserved")
    double_b_room_count = models.IntegerField(default=0, help_text="Number of B double rooms reserved")
    single_c_room_count = models.IntegerField(default=0, help_text="Number of C single rooms reserved")
    double_c_room_count = models.IntegerField(default=0, help_text="Number of C double rooms reserved")
    triple_c_room_count = models.IntegerField(default=0, help_text="Number of C triple rooms reserved")

    # For user email verification
    verification_code = models.CharField(max_length=6, blank=True, null=True, help_text="The given code during reservation")
    is_verified = models.BooleanField(default=False, help_text="Check this if the user has verified their reservation")

    guest_details = models.TextField(blank=True, null=True, help_text="CSV-like guest info: Name, AgeRange")

    def clean(self):
        """
        This method is mainly for validating that the inputted entries for the model is correct
        """
        from .utils import are_dates_available
        # Validation: End date after start
        if self.end_date <= self.start_date:
            raise ValidationError("End date must be after start date.")

        # Validation: The end date CANNOT be more than two weeks from the start date
        if self.end_date > self.start_date + timedelta(weeks=2):
            raise ValidationError("End date must only be within 2 weeks from the start date")

        # Validation: room counts cannot be all zero
        if self.is_room_count_zero(): 
            raise ValidationError("There must be 1 occupant in a room")
        # Validation: the dates inputted by the guest can be occupied
        valid_dates, total_counts = are_dates_available(self.start_date, self.end_date, self.get_room_counts(), self) 
        if not valid_dates and self.status == StatusEnum.CHECKED_IN.value: 
            raise ValidationError("Dates are unavailable for the type of room of selected; the number of selected room/s is inadequate")

        # Validation: the inputted guest count matches the inputted number of rooms
        if self.male_count + self.female_count != self.get_total_guest_count():
            raise ValidationError(f"The total guest count does not add up")

    def is_room_count_zero(self) -> bool:
        """
        This method is for determining if all the room counts are zero
        """
        return self.single_a_room_count == self.single_b_room_count == self.single_c_room_count == self.double_a_room_count == self.double_b_room_count == self.double_c_room_count == self.triple_c_room_count == 0

    def get_total_guest_count(self) -> int:
        """
        This method is primarily for getting the total guest count by getting the corresponding guest counts from the inputted room types
        """
        return self.single_a_room_count + self.single_b_room_count + self.single_c_room_count + self.double_a_room_count * 2 + self.double_b_room_count * 2  + self.double_c_room_count * 2 + self.triple_c_room_count * 3

    def get_room_counts(self) -> dict[str, int]:
        """
        This method is for getting how many rooms of each type is needed
        """
        return {
            'A': self.single_a_room_count + self.double_a_room_count,
            'B': self.single_b_room_count + self.double_b_room_count,
            'C': self.single_c_room_count + self.double_c_room_count + self.triple_c_room_count
        }

    def show_room_counts(self):
        """
        This method is for showing how many rooms of each type has been reserved
        """
        final_output = ""
        if self.single_a_room_count != 0: final_output += f"[{self.single_a_room_count} A single], "
        if self.double_a_room_count != 0: final_output += f"[{self.double_a_room_count} A double], "
        if self.single_b_room_count != 0: final_output += f"[{self.single_b_room_count} B single], "
        if self.double_b_room_count != 0: final_output += f"[{self.double_b_room_count} B double], "
        if self.single_c_room_count != 0: final_output += f"[{self.single_c_room_count} C single], "
        if self.double_c_room_count != 0: final_output += f"[{self.double_c_room_count} C double], "
        if self.triple_c_room_count != 0: final_output += f"[{self.triple_c_room_count} C triple], "
        return final_output 

    def __str__(self):
        return f"Reservation #{self.id}: {self.show_room_counts()}"

class ReservedRoom(models.Model):
    """
    Represents the reserved room of a user
    """
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, help_text="The reservation associated with this reserved room")
    room_type = models.ForeignKey(RoomType , on_delete=models.CASCADE, help_text="The room type of this reserved room")
    capacity = models.CharField(max_length=1024, choices=Capacity.choices(), blank=True, help_text="The amount of occupants in the room")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, help_text="The associated room")
    room_rate = models.ForeignKey(RoomRate, on_delete=models.CASCADE, help_text="The cost of the room at a daily rate")

    def clean(self):
        """
        This method is mainly for validating that the inputted entries for the model is correct
        """
        super().clean()

        # if the reservation is not checked in 
        # if self.reservation.status != StatusEnum.CHECKED_IN.value:
        #     raise ValidationError("You cannot use this reservation")

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
