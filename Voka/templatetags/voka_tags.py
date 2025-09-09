from django import template
from Voka.models import Direction, Services

register = template.Library()

@register.inclusion_tag('Voka/list_directions.html')
def show_directions(dir_selected=0):
    directions = Direction.objects.all()
    services = None
    if dir_selected:  # если выбрано направление
        services = Services.objects.filter(direction_id=dir_selected)
    return {"dirs": directions, "services": services, "dir_selected": dir_selected}