from django.contrib import admin
from django.urls import path, include
from Voka import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Voka.urls')),
]

