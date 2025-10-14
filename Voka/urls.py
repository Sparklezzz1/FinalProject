from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.main_page, name="main_page"),
    path('services/', views.services, name="services"),
    path('doctors/', views.doctors, name="doctors"),
    path('doc/<slug:doc_slug>/', views.show_docs, name="doc"),  
    path('news/', views.news, name="news"),
    path('news/<slug:news_slug>/', views.news_detail, name="news_detail"),
    path('serv/<slug:serv_slug>/', views.show_serv, name="serv"),
    path('appointment/', views.appointment, name='appointment'),
    path('services_form/', views.services_create, name = "services_create"),
    path('services/<int:pk>/delete/', views.service_delete, name='service_delete'),
    path('order/<int:pk>/delete/', views.order_delete, name='order_delete'),
    path('services/<int:service_id>/edit/', views.service_edit, name='service_edit'),
    path('registration/', views.Registration.as_view(), name = "registration"),
    path('profile/', views.profile, name = 'profile'),
     path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
