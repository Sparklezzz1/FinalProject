import Voka.translation  
from django.contrib import admin, messages
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
    actions = ['set_availability','del_availability']
    search_fields = ['title']
    list_filter = ['title', 'availability']

    @admin.action(description='Опубликовать выбранные услуги')
    def set_availability(self, request, queryset):
        count = queryset.update(availability = Services.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записей")

    @admin.action(description='Снять с публикации выбранные услуги')
    def del_availability(self, request, queryset):
        count = queryset.update(availability = Services.Status.DRAFT)
        self.message_user(request, f"{count} услуг снято с публикации", messages.WARNING)

@admin.register(Direction)
class DirectionAdmin(TranslationAdmin):
    list_display = ('id', 'name')
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name']


@admin.register(Order)
class OrderAdmin(TranslationAdmin):
    list_display = ('id', 'user', 'service')
    search_fields = ['user', 'service']

@admin.register(Doctors)
class DoctorsAdmin(TranslationAdmin):
    list_display = ('id', 'name', 'surname', 'job_title', 'manager')
    list_display_links = ('id', 'name', 'surname')
    ordering = ['name']
    list_editable = ('manager',)
    list_per_page = 10
    search_fields = ['name', 'surname', 'job_title',]
    list_filter = ['surname', 'job_title']


@admin.register(Appointment)
class AppointmentAdmin(TranslationAdmin):
    list_display = ('id', 'patient_name', 'patient_surname', 'reason')
    search_fields = ['patient_name', 'patient_surname', 'reason']

@admin.register(News)
class NewsAdmin(TranslationAdmin):
    list_display = ('id', 'title')
    search_fields = ['title']
