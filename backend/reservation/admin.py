from django.contrib import admin
from .models import Reservation, ReservedRoom

# Register your models here.
admin.site.register(Reservation)
admin.site.register(ReservedRoom)
