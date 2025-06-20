from django.contrib import admin
from .models import Guest

class GuestAdmin(admin.ModelAdmin):
    list_display = ('email_address', 'name', 'phone_number')

# Register your models here.
admin.site.register(Guest, GuestAdmin)
