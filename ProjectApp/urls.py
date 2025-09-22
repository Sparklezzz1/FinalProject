from django.contrib import admin
from django.urls import path, include
from Voka import views
from Voka.views import page_not_found
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Voka.urls')),
] 

handler404 = page_not_found