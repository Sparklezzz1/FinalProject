from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name = "mains_page"),
    path('about/', views.about, name = "about"),
    path('services/', views.services, name = "services"),
    path('price_list/', views.price_list, name = "price_list"),
    path('doctors/', views.doctors, name = "doctors"),
    path('doc/<slug:doc_slug>/', views.show_docs, name = "show_docs"),
    path('news/', views.news, name = "news"),
    path('login/', views.login, name = "login"),
    path('contacts/', views.contacts, name = "contacts"),
    path('serv/<slug:serv_slug>/', views.show_serv, name = "serv"),
    path('direction/<slug:direction_slug>/', views.show_direction, name='show_direction'),
]