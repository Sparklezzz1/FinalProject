from django import template
from Voka.models import Direction, Services

register = template.Library()

@register.inclusion_tag('Voka/list_directions.html')
def show_directions(dir_selected=0):
    directions = Direction.objects.all()
    return {"dirs": directions, "dir_selected": dir_selected}