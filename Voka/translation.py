from modeltranslation.translator import register, TranslationOptions
from .models.services import Services, Direction
from .models.doctors import Doctors
from .models.news import News
from .models.appointment import Appointment

@register(Services)
class ServicesTranslationOptions(TranslationOptions):
    fields = ('title', 'content') 

@register(Direction)
class DirectionTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Doctors)
class DoctorsTranslationOptions(TranslationOptions):
    fields = ('name', 'surname', 'patronymic', 'job_title')

@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'content')

@register(Appointment)
class AppointmentTranslationOptions(TranslationOptions):
    fields = ('patient_name','patient_surname', 'reason','doctor')