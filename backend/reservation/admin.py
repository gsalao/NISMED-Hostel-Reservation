from django.contrib import admin
from .models import Reservation, ReservedRoom

class ReservedRoomInline(admin.TabularInline):
    model = ReservedRoom
    extra = 1 
    class Media:
        js = (
            'inline-room-dropdown-select.js', 
            'https://code.jquery.com/jquery-3.3.1.min.js' 
        )

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'guest_id', 'status', 'reservation_date', 'start_date', 'end_date', 'assigned_a_room')
    list_editable = ('status', 'assigned_a_room')
    list_filter = ('guest_id', 'status', 'reservation_date')
    list_per_page = 10
    inlines = [ReservedRoomInline]

class ReservedRoomAdmin(admin.ModelAdmin):
    list_display = ('reservation', 'start_date', 'end_date', 'room_type', 'room', 'room_rate',) 
    list_filter = ('reservation', 'reservation__start_date', 'reservation__end_date', 'room_type', 'room')
    list_per_page = 10

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

