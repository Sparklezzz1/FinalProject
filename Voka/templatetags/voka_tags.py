from django import template
import Voka.views as views

register = template.Library()


@register.simple_tag(name='getserv')
def get_services():
    return views.serv_db

@register.inclusion_tag('Voka/list_services.html')
def show_services():
    servs = views.serv_db
    return {'servs' : servs}
