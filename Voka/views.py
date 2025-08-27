from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.template.loader import render_to_string

menu = [
    {'title' : 'О центе', 'url_name' : 'about'},
    {'title' : 'Услуги', 'url_name' : 'services'},
    {'title' : 'Цены', 'url_name' : 'price_list'},
    {'title' : 'Врачи', 'url_name' : 'doctors'},
    {'title' : 'Новости', 'url_name' : 'news'},
    {'title' : 'Контакты', 'url_name' : 'contacts'},
    {'title' : 'Авторизация', 'url_name' : 'login'},
]

data_db = [
    {'id' : 1, 'title' : 'Лазерная коррекция зрения', 'price' : 'от 1200 руб.', 'availability' : True},
    {'id' : 2, 'title' : 'Лечение катаракты', 'price' : 'от 900 руб.', 'availability' : False},
    {'id' : 3, 'title' : 'Диагностика', 'price' : 'от 70 руб.', 'availability' : True}
]
def main_page(request):
    data ={
        'title':'Главная страница',
        'menu': menu,
        "services":data_db,
        }
    return render(request,'Voka/main_page.html', context = data)

def services(request):
    return render(request, 'Voka/services.html',{'title' : 'Услуги', 'menu' : menu})

def show_serv(request, serv_id):
    return HttpResponse(f"Отображение услуг с id = {serv_id}")

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