
from django.urls import path
from . import views

urlpatterns = [
    path('insert_guest/', views.insert_guest, name='insert_guests'),
]
