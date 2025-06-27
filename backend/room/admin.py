from django.contrib import admin
from .models import Room, RoomType, RoomRate 

class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'available_rooms') 
    list_editable = ('available_rooms',) 
    list_per_page = 10

class RoomRateAdmin(admin.ModelAdmin):
    list_display = ('room_type_id', 'occupancy', 'rate') 
    list_filter = ('room_type_id', 'occupancy')
    list_per_page = 10

class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type_id', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('room_type_id',)
    list_per_page = 10

# Register your models here.
admin.site.register(Room, RoomAdmin)
admin.site.register(RoomType, RoomTypeAdmin)
admin.site.register(RoomRate, RoomRateAdmin)
