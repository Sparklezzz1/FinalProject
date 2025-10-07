from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.main_page, name="main_page"),
    path('about/', views.about, name="about"),
    path('services/', views.services, name="services"),
    path('doctors/', views.doctors, name="doctors"),
    path('doc/<slug:doc_slug>/', views.show_docs, name="doc"),  
    path('news/', views.news, name="news"),
    path('serv/<slug:serv_slug>/', views.show_serv, name="serv"),
    path('appointment/', views.appointment, name='appointment'),
    path('appointment/<int:service_id>/', views.appointment, name='appointment_with_service'),
    path('services_form/', views.services_create, name = "services_create"),
    path('services/<int:pk>/delete/', views.service_delete, name='service_delete'),
    path('services/<int:service_id>/edit/', views.service_edit, name='service_edit'),
    path('registration/', views.Registration.as_view(), name = "registration"),
    path('profile/', views.profile, name = 'profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
