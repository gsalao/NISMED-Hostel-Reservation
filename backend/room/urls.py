
from django.urls import path
from . import views

urlpatterns = [
    path('get_all_rooms/', views.get_all_rooms, name='get_all_rooms'),
    path('get_all_room_types/', views.get_all_room_types, name='get_room_types'),
    path('get_all_room_rates/', views.get_all_room_rates, name='get_all_room_rates'),
]
