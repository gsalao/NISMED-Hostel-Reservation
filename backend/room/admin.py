from django.contrib import admin
from .models import Room, RoomType, RoomRate 

# Register your models here.
admin.site.register(Room)
admin.site.register(RoomType)
admin.site.register(RoomRate)
