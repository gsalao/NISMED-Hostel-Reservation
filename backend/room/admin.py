from django.contrib import admin
from .models import Room, RoomType, RoomRate, Amenity, RoomTypeImage

class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'available_rooms') 
    ordering = ('name',)
    list_per_page = 10
    filter_horizontal = ('amenities',)

class RoomRateAdmin(admin.ModelAdmin):
    list_display = ('room_type', 'occupancy', 'rate') 
    list_filter = ('room_type', 'occupancy')
    ordering = ('-room_type', 'occupancy')
    list_per_page = 10

class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('room_type',)
    ordering = ('room_number', '-room_type',)
    list_per_page = 10

class RoomTypeImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'room_type')
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if obj.image and hasattr(obj.image.file, 'close'):
            obj.image.file.close()

# Register your models here.
admin.site.register(Room, RoomAdmin)
admin.site.register(RoomType, RoomTypeAdmin)
admin.site.register(RoomRate, RoomRateAdmin)
admin.site.register(Amenity)
admin.site.register(RoomTypeImage)
