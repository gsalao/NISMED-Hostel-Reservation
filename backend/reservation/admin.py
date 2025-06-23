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
    inlines = [ReservedRoomInline]

class ReservedRoomAdmin(admin.ModelAdmin):
    list_display = ('reservation', 'room_type', 'room', 'room_rate',) 
    class Media:
        js = (
            'room-dropdown-select.js', 
            'https://code.jquery.com/jquery-3.3.1.min.js' 
        )

# Register your models here.
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(ReservedRoom, ReservedRoomAdmin)

