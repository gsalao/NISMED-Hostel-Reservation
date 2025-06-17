
from django.urls import path
from . import views

urlpatterns = [
    path('get_all_guests/', views.get_all_guests, name='all_guests'),
    path('insert_guest/', views.insert_guest, name='insert_guests'),
]
