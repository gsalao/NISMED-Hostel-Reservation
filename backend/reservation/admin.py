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
    list_display = ('reservation', 'room', 'room_rate',) 

# Register your models here.
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(ReservedRoom, ReservedRoomAdmin)

