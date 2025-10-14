import Voka.translation  
from django.contrib import admin
from .models.services import Services, Direction, Order
from .models.doctors import Doctors
from .models.appointment import Appointment
from .models.news import News
from modeltranslation.admin import TranslationAdmin

@admin.register(Services)
class ServicesAdmin(TranslationAdmin):
    list_display = ('id', 'title', 'time_create', 'availability')
    prepopulated_fields = {"slug": ("title",)}
    list_display_links = ('id', 'title')
    ordering = ['time_create', 'title']
    list_editable = ('availability',)
    list_per_page = 5

@admin.register(Direction)
class DirectionAdmin(TranslationAdmin):
    list_display = ('id', 'name')
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Order)
class OrderAdmin(TranslationAdmin):
    list_display = ('id', 'user', 'service')

@admin.register(Doctors)
class DoctorsAdmin(TranslationAdmin):
    list_display = ('id', 'name', 'surname', 'job_title', 'manager')
    list_display_links = ('id', 'name', 'surname')
    ordering = ['name']
    list_editable = ('manager',)
    list_per_page = 10

@admin.register(Appointment)
class AppointmentAdmin(TranslationAdmin):
    list_display = ('id', 'patient_name', 'patient_surname', 'reason')

@admin.register(News)
class NewsAdmin(TranslationAdmin):
    list_display = ('id', 'title')
