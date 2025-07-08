from django.contrib import admin
from django import forms
from .models import Reservation, ReservedRoom
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError

class ReservedRoomInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        seen_rooms = set()
        for form in self.forms:
            if form.cleaned_data.get('DELETE'):
                continue

            room = form.cleaned_data.get('room')
            if room in seen_rooms:
                raise ValidationError(f"Room '{room}' has been selected more than once in this reservation.")
            seen_rooms.add(room)

class ReservedRoomInline(admin.TabularInline):
    model = ReservedRoom
    formset = ReservedRoomInlineFormSet
    extra = 1 
    verbose_name = "Assign room/s"
    verbose_name_plural = "Assign room/s"
    class Media:
        js = (
            'inline-room-dropdown-select.js', 
            'https://code.jquery.com/jquery-3.3.1.min.js' 
        )

class ReservedRoomForm(forms.ModelForm):
    class Meta:
        model = ReservedRoom
        fields = ['reservation', 'room_type', 'capacity', 'room', 'room_rate']

    def clean(self):
        cleaned_data = super().clean()
        reservation = cleaned_data.get('reservation')
        room = cleaned_data.get('room')

        if reservation and room:
            # Check for other reserved rooms for the same reservation using the same room
            qs = ReservedRoom.objects.filter(reservation=reservation, room=room)

            # Exclude current instance when updating
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise ValidationError(f"Room '{room}' has already been assigned to this reservation.")

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'guest', 'status', 'reservation_date', 'start_date', 'end_date', 'assigned_a_room')
    list_editable = ('status', 'assigned_a_room')
    list_filter = ('guest', 'status', 'reservation_date')
    list_per_page = 10
    inlines = [ReservedRoomInline]

class ReservedRoomAdmin(admin.ModelAdmin):
    list_display = ('reservation', 'start_date', 'end_date', 'room_type', 'capacity', 'room', 'room_rate', ) 
    list_editable = ('capacity', )
    list_filter = ('reservation', 'reservation__start_date', 'reservation__end_date', 'room_type', 'room')
    list_per_page = 10
    form = ReservedRoomForm

    def start_date(self, obj):
        return obj.reservation.start_date

    start_date.admin_order_field = 'reservation__start_date'
    start_date.short_description = 'Start Date'

    def end_date(self, obj):
        return obj.reservation.end_date
    end_date.admin_order_field = 'reservation__end_date'
    end_date.short_description = 'End Date'

    class Media:
        js = (
            'room-dropdown-select.js', 
            'https://code.jquery.com/jquery-3.3.1.min.js' 
        )

# Register your models here.
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(ReservedRoom, ReservedRoomAdmin)

