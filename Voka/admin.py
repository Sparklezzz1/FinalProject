from django.contrib import admin
from .models.services import Services
from .models.services import Direction
from .models.doctors import Doctors
from .models.appointment import Appointment

# Register your models here.
admin.site.register(Services)
admin.site.register(Doctors)
admin.site.register(Direction)
admin.site.register(Appointment)