from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import GuestSerializer 
from .models import Guest 

# Create your views here.
