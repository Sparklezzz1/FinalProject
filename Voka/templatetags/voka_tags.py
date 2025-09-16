from django import template
from Voka.models import Direction, Services, Doctors

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