from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name="main_page"),
    path('about/', views.about, name="about"),
    path('services/', views.services, name="services"),
    path('doctors/', views.doctors, name="doctors"),
    path('doc/<slug:doc_slug>/', views.show_docs, name="doc"),  
    path('news/', views.news, name="news"),
    path('login/', views.login, name="login"),
    path('contacts/', views.contacts, name="contacts"),
    path('serv/<slug:serv_slug>/', views.show_serv, name="serv"),
    path('appointment/', views.appointment, name = "appointment"),
    path('services_form/', views.services_create, name = "services_create"),
    path('services/<int:pk>/delete/', views.service_delete, name='service_delete'),
    path('services/<int:service_id>/edit/', views.service_edit, name='service_edit'),
]
