"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse, HttpResponseForbidden
from django.db import connection
from django.db.utils import OperationalError
from decouple import config

HEALTH_CHECK_TOKEN = config('HEALTH_CHECK_TOKEN')
def ping(request):
   return JsonResponse({
        "status": "ok",
    })

def ping_db(request):
    token = request.GET.get("token")
    if token != HEALTH_CHECK_TOKEN:
        return HttpResponseForbidden("Forbidden")

    db_status = "unknown"
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            db_status = "ok"
    except OperationalError:
        db_status = "unavailable"

    return JsonResponse({
        "status": "ok",
        "database": db_status
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/guest/', include('guest.urls')),
    path('api/reserve/', include('reservation.urls')),
    path('api/room/', include('room.urls')),
    path('ping/', ping),
    path('ping/db', ping_db)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
