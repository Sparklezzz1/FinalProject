from django import template
from django.contrib import admin
from Voka.models.services import Direction
from Voka.models.doctors import Doctors

register = template.Library()

@register.inclusion_tag('Voka/list_directions.html')
def show_directions():
    directions = Direction.objects.all()
    return {"dirs": directions}

@register.inclusion_tag('Voka/list_docs.html')
def show_docs(docs=None):
    if docs is None:
        docs = Doctors.objects.all()
    return {"docs": docs}