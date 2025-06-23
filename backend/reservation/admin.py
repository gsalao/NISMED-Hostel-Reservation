from django.contrib import admin
from .models import Reservation, ReservedRoom

class ReservedRoomInline(admin.TabularInline):
    model = ReservedRoom
    extra = 1 

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('guest_id', 'status', 'reservation_date', 'start_date', 'end_date')
    list_editable = ('status',)
    list_filter = ('guest_id', 'status', 'reservation_date')
    inlines = [ReservedRoomInline]

class ReservedRoomAdmin(admin.ModelAdmin):
    list_display = ('reservation', 'room_type', 'room', 'room_rate',) 
    class Media:
        js = (
            'room-dropdown-select.js', # In your static folder and write the logic in this file.
            'https://code.jquery.com/jquery-3.3.1.min.js' # Jquery CDN
        )

# Register your models here.
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(ReservedRoom, ReservedRoomAdmin)

