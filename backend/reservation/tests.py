from django.test import TestCase
from .models import Reservation, ReservedRoom, StatusEnum
from guest.models import Guest 
from room.models import RoomType, RoomRate, Room
from django.core.exceptions import ValidationError
from datetime import timedelta, date

# Create your tests here.
class ReservationTestCase(TestCase):
    def setUp(self):
        self.today = date.today()
        self.tomorrow = self.today + timedelta(days=1)
        self.after_tomorrow = self.today + timedelta(days=2)
        self.over_two_weeks = self.today + timedelta(days=15)

        self.a = RoomType.objects.create(name='A', available_rooms=1)
        self.b = RoomType.objects.create(name='B', available_rooms=2)
        self.c = RoomType.objects.create(name='C', available_rooms=3)

        self.room_a1 = Room.objects.create(room_type=self.a, room_number=101, is_active=True)
        self.room_b1 = Room.objects.create(room_type=self.b, room_number=201, is_active=True)
        self.room_c1 = Room.objects.create(room_type=self.c, room_number=301, is_active=True)
        self.room_b2 = Room.objects.create(room_type=self.b, room_number=202, is_active=True)
        self.room_c2 = Room.objects.create(room_type=self.c, room_number=302, is_active=True)
        self.room_c3 = Room.objects.create(room_type=self.c, room_number=303, is_active=True)

        self.a1 = RoomRate.objects.create(room_type=self.a, occupancy=1, rate=1000.00)
        self.a2 = RoomRate.objects.create(room_type=self.a, occupancy=2, rate=1500.00)
        self.b1 = RoomRate.objects.create(room_type=self.b, occupancy=1, rate=2000.00)
        self.b2 = RoomRate.objects.create(room_type=self.b, occupancy=2, rate=2500.00)
        self.c1 = RoomRate.objects.create(room_type=self.c, occupancy=1, rate=500.00)
        self.c2 = RoomRate.objects.create(room_type=self.c, occupancy=2, rate=750.00)
        self.c3 = RoomRate.objects.create(room_type=self.c, occupancy=3, rate=1000.00)

        self.guest_1 = Guest.objects.create(email_address="test@example.com", phone_number="0999 999 9999", address="UP Diliman", name="Juan Dela Cruz")

    def create_reservation(self, **kwargs):
        data = {
            "guest": self.guest_1,
            "start_date": self.today,
            "end_date": self.tomorrow,
            "for_person_name": "Juan Dela Cruz",
            "male_count": 1,
            "female_count": 0,
            "single_a_room_count": 1,
            "double_a_room_count": 0,
            "single_b_room_count": 0,
            "double_b_room_count": 0,
            "single_c_room_count": 0,
            "double_c_room_count": 0,
            "triple_c_room_count": 0,
            "status": StatusEnum.CHECKED_IN.value,
        }
        data.update(kwargs)
        return Reservation(**data)

    def test_valid_reservation(self):
        reservation = self.create_reservation()
        try:
            reservation.full_clean()
        except ValidationError:
            self.fail("Valid reservation should not raise ValidationError")

    def test_multiple_valid_reservation_different_rooms(self):
        reservation_1 = self.create_reservation()
        reservation_2 = self.create_reservation(single_a_room_count=0, single_b_room_count=2, male_count=2)
        reservation_3 = self.create_reservation(single_a_room_count=0, single_c_room_count=3, male_count=2, female_count=1)
        try:
            reservation_1.full_clean()
            reservation_2.full_clean()
            reservation_3.full_clean()
        except ValidationError:
            self.fail("Valid reservations should not raise ValidationError")

    def test_multiple_valid_reservation_same_rooms(self):
        reservation_1 = self.create_reservation(single_a_room_count=0, single_c_room_count=2, male_count=2)
        reservation_2 = self.create_reservation(single_a_room_count=0, single_c_room_count=1, male_count=0, female_count=1)
        try:
            reservation_1.full_clean()
            reservation_2.full_clean()
        except ValidationError:
            self.fail("Valid reservations should not raise ValidationError")

    def test_multiple_valid_reservations_diff_dates(self):
        reservation_1 = self.create_reservation()
        reservation_2 = self.create_reservation(start_date=self.tomorrow, end_date=self.after_tomorrow)
        try:
            reservation_1.full_clean()
            reservation_2.full_clean()
        except ValidationError:
            self.fail("Valid reservations should not raise ValidationError")

    def test_valid_reservation_with_one_cancelled(self):
        reservation_1 = self.create_reservation(status=StatusEnum.CHECKED_OUT.value,)
        reservation_2 = self.create_reservation()
        try:
            reservation_1.full_clean()
            reservation_2.full_clean()
        except ValidationError:
            self.fail("Valid reservations should not raise ValidationError")

    def test_reservation_exactly_two_weeks(self):
        # Exactly 2 weeks should be allowed
        reservation = self.create_reservation(end_date=self.today + timedelta(weeks=2))
        try:
            reservation.full_clean()
        except ValidationError:
            self.fail("Exactly two weeks reservation should be allowed")

    def test_invalid_number_of_guests(self):
        reservation= self.create_reservation(male_count=2)
        with self.assertRaises(ValidationError) as ctx:
            reservation.full_clean()
        self.assertIn("The total guest count does not add up", str(ctx.exception))

    def test_end_date_before_start_date(self):
        reservation = self.create_reservation(end_date=self.today - timedelta(days=1))
        with self.assertRaises(ValidationError) as ctx:
            reservation.full_clean()
        self.assertIn("End date must be after start date.", str(ctx.exception))

    def test_zero_night_reservation(self):
        reservation = self.create_reservation(start_date=self.today, end_date=self.today)
        with self.assertRaises(ValidationError) as ctx:
            reservation.full_clean()
        self.assertIn("End date must be after start date", str(ctx.exception))

    def test_stay_exceeds_two_weeks(self):
        reservation = self.create_reservation(end_date=self.over_two_weeks)
        with self.assertRaises(ValidationError) as ctx:
            reservation.full_clean()
        self.assertIn("End date must only be within 2 weeks", str(ctx.exception))

    def test_all_zero_room_counts(self):
        reservation = self.create_reservation(
            single_a_room_count=0, double_a_room_count=0,
            single_b_room_count=0, double_b_room_count=0,
            single_c_room_count=0, double_c_room_count=0,
            triple_c_room_count=0
        )
        with self.assertRaises(ValidationError) as ctx:
            reservation.full_clean()
        self.assertIn("There must be 1 occupant in a room", str(ctx.exception))

    def test_reserved_room_with_unavailable_room(self):
        # First reservation with room_a1
        res1 = self.create_reservation()
        res1.save()
        ReservedRoom.objects.create(
            reservation=res1,
            room_type=self.a,
            room=self.room_a1,
            room_rate=self.a1
        )

        # Overlapping reservation using same room
        res2 = self.create_reservation(start_date=self.today, end_date=self.after_tomorrow)
        res2.save()

        conflict = ReservedRoom(
            reservation=res2,
            room_type=self.a,
            room=self.room_a1,
            room_rate=self.a1
        )

        with self.assertRaises(ValidationError) as ctx:
            conflict.full_clean()
        self.assertIn("already reserved during the selected period", str(ctx.exception))

    def test_reserved_room_invalid_status(self):
        res = self.create_reservation(status=StatusEnum.CANCELLED.value)
        res.save()

        reserved_room = ReservedRoom(
            reservation=res,
            room_type=self.a,
            room=self.room_a1,
            room_rate=self.a1
        )

        with self.assertRaises(ValidationError) as ctx:
            reserved_room.full_clean()
        self.assertIn("You cannot use this reservation", str(ctx.exception))

    def test_too_many_reserved_rooms(self):
        res1 = self.create_reservation(single_a_room_count=0, single_b_room_count=2,male_count=2)
        res1.save()
        res2 = self.create_reservation(single_a_room_count=0, single_b_room_count=1)
        with self.assertRaises(ValidationError) as ctx:
            res2.full_clean()
        self.assertIn("The reservation cannot be made; You cannot reserve your listed amount of: B room/s", str(ctx.exception))

    def test_reservation_set_with_start_date_before(self):
        res1 = self.create_reservation()
        res1.save()
        res2 = self.create_reservation(start_date=self.today - timedelta(days=1), end_date = self.tomorrow)
        with self.assertRaises(ValidationError) as ctx:
            res2.full_clean()
        self.assertIn("The reservation cannot be made; You cannot reserve your listed amount of: A room/s", str(ctx.exception))

    def test_reservation_set_with_start_date_during(self):
        res1 = self.create_reservation(start_date=self.today, end_date=self.after_tomorrow)
        res1.save()
        res2 = self.create_reservation(start_date=self.tomorrow, end_date = self.after_tomorrow + timedelta(days=1))
        with self.assertRaises(ValidationError) as ctx:
            res2.full_clean()
        self.assertIn("The reservation cannot be made; You cannot reserve your listed amount of: A room/s", str(ctx.exception))

    def test_reservation_set_with_covers_everything(self):
        res1 = self.create_reservation(start_date=self.today, end_date=self.after_tomorrow)
        res1.save()
        res2 = self.create_reservation(start_date=self.today - timedelta(days=1), end_date=self.after_tomorrow + timedelta(days=1))
        with self.assertRaises(ValidationError) as ctx:
            res2.full_clean()
        self.assertIn("The reservation cannot be made; You cannot reserve your listed amount of: A room/s", str(ctx.exception))

    def test_multiple_reservation_full_rooms_a(self):
        reservation_1 = self.create_reservation()
        reservation_2 = self.create_reservation()
        reservation_3 = self.create_reservation(single_a_room_count=0, single_b_room_count=1, male_count=1)
        reservation_1.save()
        reservation_3.save()
        with self.assertRaises(ValidationError) as ctx:
            reservation_2.full_clean()
        self.assertIn("The reservation cannot be made; You cannot reserve your listed amount of: A room/s", str(ctx.exception))

    def test_multiple_reservation_full_rooms_b(self):
        reservation_1 = self.create_reservation()
        reservation_2 = self.create_reservation(single_a_room_count=0, single_b_room_count=2, male_count=2)
        reservation_3 = self.create_reservation(single_a_room_count=0, single_b_room_count=1, male_count=1)
        reservation_1.save()
        reservation_2.save()
        with self.assertRaises(ValidationError) as ctx:
            reservation_3.full_clean()
        self.assertIn("The reservation cannot be made; You cannot reserve your listed amount of: B room/s", str(ctx.exception))
        
    def test_multiple_reservation_full_rooms_c(self):
        reservation_1 = self.create_reservation()
        reservation_2 = self.create_reservation(single_a_room_count=0, single_c_room_count=2, male_count=2)
        reservation_3 = self.create_reservation(single_a_room_count=0, single_c_room_count=1, male_count=1)
        reservation_4 = self.create_reservation(single_a_room_count=0, single_c_room_count=1, male_count=1)
        reservation_1.save()
        reservation_2.save()
        reservation_3.save()
        with self.assertRaises(ValidationError) as ctx:
            reservation_4.full_clean()
        self.assertIn("The reservation cannot be made; You cannot reserve your listed amount of: C room/s", str(ctx.exception))

    def test_multiple_reservation_full_rooms_double_b(self):
        reservation_1 = self.create_reservation()
        reservation_2 = self.create_reservation(single_a_room_count=0, double_b_room_count=2, male_count=2)
        reservation_3 = self.create_reservation(single_a_room_count=0, double_b_room_count=1, male_count=1)
        reservation_1.save()
        reservation_2.save()
        with self.assertRaises(ValidationError) as ctx:
            reservation_3.full_clean()
        self.assertIn("The reservation cannot be made; You cannot reserve your listed amount of: B room/s", str(ctx.exception))

    def test_multiple_reservation_full_rooms_double_c(self):
        reservation_1 = self.create_reservation()
        reservation_2 = self.create_reservation(single_a_room_count=0, double_c_room_count=2, male_count=2)
        reservation_3 = self.create_reservation(single_a_room_count=0, double_c_room_count=1, male_count=1)
        reservation_4 = self.create_reservation(single_a_room_count=0, double_c_room_count=1, male_count=1)
        reservation_1.save()
        reservation_2.save()
        reservation_3.save()
        with self.assertRaises(ValidationError) as ctx:
            reservation_4.full_clean()
        self.assertIn("The reservation cannot be made; You cannot reserve your listed amount of: C room/s", str(ctx.exception))

    def test_multiple_reservation_full_rooms_exceed_everything(self):
        reservation_1 = self.create_reservation()
        reservation_2 = self.create_reservation(single_a_room_count=0, double_b_room_count=2, male_count=2)
        reservation_3 = self.create_reservation(single_a_room_count=0, single_c_room_count=3, male_count=3)
        reservation_4 = self.create_reservation(double_b_room_count=2, single_c_room_count=1, male_count=6)
        reservation_1.save()
        reservation_2.save()
        reservation_3.save()
        with self.assertRaises(ValidationError) as ctx:
            reservation_4.full_clean()
        self.assertIn("The reservation cannot be made; You cannot reserve your listed amount of: A room/sB room/sC room/s", str(ctx.exception))

    def test_end_date_edited_with_reservation_made_previously(self):
        reservation_1 = self.create_reservation()
        reservation_2 = self.create_reservation(start_date=self.tomorrow, end_date=self.after_tomorrow)
        reservation_1.save()
        reservation_2.save()
        with self.assertRaises(ValidationError) as ctx:
            reservation_1.end_date = self.after_tomorrow
            reservation_1.full_clean()
        self.assertIn("The reservation cannot be made; You cannot reserve your listed amount of: A room/s", str(ctx.exception))

    def test_invalid_gender_distribution(self):
        # 1 male in a triple room should be invalid
        reservation = self.create_reservation(
            single_a_room_count=0,
            triple_c_room_count=1,
            male_count=1,
            female_count=0
        )
        with self.assertRaises(ValidationError) as ctx:
            reservation.full_clean()
        self.assertIn("The total guest count does not add up", str(ctx.exception))

    def test_room_capacity_exceeded(self):
        # Trying to put 3 people in a single room
        reservation = self.create_reservation(
            single_a_room_count=1,
            male_count=3,
            female_count=0
        )
        with self.assertRaises(ValidationError) as ctx:
            reservation.full_clean()
        self.assertIn("The total guest count does not add up", str(ctx.exception))

    def test_mixed_room_type_reservation(self):
        # Reserve one A room and one B room
        reservation = self.create_reservation(
            single_a_room_count=1,
            single_b_room_count=1,
            male_count=2
        )
        try:
            reservation.full_clean()
        except ValidationError:
            self.fail("Mixed room type reservation should be allowed")

    def test_room_availability_after_reservation_deletion(self):
        # Create and delete a reservation, then try to reuse the room
        res1 = self.create_reservation()
        res1.save()
        res1.delete()
        
        # Should be able to reuse the room now
        res2 = self.create_reservation()
        try:
            res2.full_clean()
            res2.save()
        except ValidationError:
            self.fail("Should be able to reserve after previous reservation is deleted")
