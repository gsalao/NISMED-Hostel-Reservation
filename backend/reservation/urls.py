from django.urls import path
from . import views

urlpatterns = [
    path('create_new_reservation/', views.create_new_reservation, name='create_new_reservation'),
    path('verify_reservation/', views.verify_reservation, name='verify_reservation'),
    path('get_reservation_email/', views.get_reservation_email, name='get_email_reservation'),
]
