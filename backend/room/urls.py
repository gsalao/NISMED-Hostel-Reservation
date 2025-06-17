
from django.urls import path
from . import views

urlpatterns = [
    path('create_new_room_type/', views.create_new_room_type, name='new_room_type'),
    path('create_new_room/', views.create_new_room, name='new_room'),
    path('create_new_room_rate/', views.create_new_room_rate, name='new_room_rate'),
    path('change_room_type_inventory/', views.change_room_type_inventory, name='change_room_type_inventory'),
    path('change_room_rate/', views.change_room_rate, name='change_room_rate'),
]
