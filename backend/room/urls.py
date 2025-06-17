
from django.urls import path
from . import views

urlpatterns = [
    path('get_all_rooms/', views.get_all_rooms, name='get_all_rooms'),
    path('get_all_room_types/', views.get_all_room_types, name='get_room_types'),
    path('get_all_room_rates/', views.get_all_room_rates, name='get_all_room_rates'),
    path('create_new_room_type/', views.create_new_room_type, name='new_room_type'),
    path('create_new_room/', views.create_new_room, name='new_room'),
    path('create_new_room_rate/', views.create_new_room_rate, name='new_room_rate'),
    path('change_room_type_inventory/', views.change_room_type_inventory, name='change_room_type_inventory'),
    path('change_room_rate/', views.change_room_rate, name='change_room_rate'),
]
