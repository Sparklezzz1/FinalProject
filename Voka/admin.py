from django.contrib import admin
from .models.services import Services
from .models.services import Direction
from .models.services import Order
from .models.doctors import Doctors
from .models.appointment import Appointment
from .models.news import News

@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'availability')
    prepopulated_fields = {"slug": ("title",)}
    list_display_links = ('id', 'title')
    ordering = ['time_create', 'title']
    list_editable = ('availability',)
    list_per_page = 5

@admin.register(Doctors)
class DoctorsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'job_title', 'manager')
    list_display_links = ('id', 'name', 'surname')
    ordering = ['name']
    list_editable = ('manager',)
    list_per_page = 10

admin.site.register(Direction)
admin.site.register(Appointment)
admin.site.register(Order)
admin.site.register(News)
