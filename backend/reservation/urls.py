
from django.urls import path
from . import views

urlpatterns = [
    path('get_all_reservation_status/', views.get_all_reservation_status, name='get_all_reservation_status'),
    path('create_new_reservation/', views.create_new_reservation, name='create_new_reservation'),
    path('change_reservation_status/', views.change_reservation_status, name='change_reservation_status'),
]
