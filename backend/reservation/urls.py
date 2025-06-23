from django.urls import path
from . import views

urlpatterns = [
    path('create_new_reservation/', views.create_new_reservation, name='create_new_reservation'),
]
