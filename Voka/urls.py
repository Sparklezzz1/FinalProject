from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name = "mains_page"),
    path('serv/', views.services, name = "serv"),
    path("serv/<int:serv_id>", views.services_by_id, name = "servs_id"),
    path("serv/<slug:serv_slug>", views.services_by_slug, name = "servs_slug"),
]