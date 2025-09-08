from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseNotFound
from django.template.loader import render_to_string
from .models import Services

menu = [
    {'title' : 'О центре', 'url_name' : 'about'},
    {'title' : 'Услуги', 'url_name' : 'services'},
    {'title' : 'Цены', 'url_name' : 'price_list'},
    {'title' : 'Врачи', 'url_name' : 'doctors'},
    {'title' : 'Новости', 'url_name' : 'news'},
    {'title' : 'Контакты', 'url_name' : 'contacts'},
    {'title' : 'Авторизация', 'url_name' : 'login'},
]


serv_db = [
    {'id': 1, 'name': 'Обследование'},
    {'id': 2, 'name': 'Консультация'},
    {'id': 3, 'name': 'Хирургия'},
]

def main_page(request):
    services = Services.objects.filter(availability = 1)
    data ={
        'title':'Главная страница',
        'menu': menu,
        'services': services,
        }
    return render(request,'Voka/main_page.html', context = data)

def services(request):
    services = Services.objects.filter(availability = 1)
    data ={
        'title':'Главная страница',
        'menu': menu,
        'services': services,
        }
    return render(request, 'Voka/services.html',{'title' : 'Услуги', 'menu' : menu, 'services': services})

def show_serv(request, serv_slug):
    serv = get_object_or_404(Services, slug = serv_slug)
    data = {
        'title' : serv.title,
        'menu' : menu,
        'serv' : serv,
        'cat_selected' : 1,

    }
    return render(request,'Voka/serv.html', data)

def show_stock(request, stock_id):
    return HttpResponse(f"Отображение акции с id = {stock_id}")

def about(request):
    return HttpResponse("О нас")

def price_list(request):
    return HttpResponse("Цены")

def doctors(request):
    return HttpResponse("Врачи")

def news(request):
    return HttpResponse("Новости")

def login(request):
    return HttpResponse("Авторизация")

def contacts(request):
    return HttpResponse("Контакты")

def page_not_found(request, exception):
    return HttpResponseNotFound(render(request, 'Voka/page_not_found.html'))