from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseNotFound
from django.template.loader import render_to_string
from .models import Direction, Services, Doctors

menu = [
    {'title' : 'О центре', 'url_name' : 'about'},
    {'title' : 'Услуги', 'url_name' : 'services'},
    {'title' : 'Цены', 'url_name' : 'price_list'},
    {'title' : 'Врачи', 'url_name' : 'doctors'},
    {'title' : 'Новости', 'url_name' : 'news'},
    {'title' : 'Контакты', 'url_name' : 'contacts'},
    {'title' : 'Авторизация', 'url_name' : 'login'},
]


def main_page(request):
    services = Services.objects.filter(availability = Services.Status.PUBLISHED)
    data ={
        'title':'Главная страница',
        'menu': menu,
        'services': services,
        }
    return render(request,'Voka/main_page.html', context = data)

def services(request):
    services = Services.objects.filter(availability=Services.Status.PUBLISHED)
    doc_slug = request.GET.get('doctor')
    if doc_slug:
        selected_doc = get_object_or_404(Doctors, slug=doc_slug)
        services = services.filter(doctors=selected_doc)
    else:
        selected_doc = None

    context = {
        'title': 'Услуги',
        'menu': menu,
        'services': services,
        'selected_doc': selected_doc,
    }
    return render(request, 'Voka/services.html', context)

def show_serv(request, serv_slug):
    serv = get_object_or_404(Services, slug = serv_slug)
    doctors = serv.doctors.all()
    data = {
        'title' : serv.title,
        'menu' : menu,
        'serv' : serv,
         'doctors': doctors,
    }
    return render(request,'Voka/serv.html', data)

def show_direction(request, direction_slug):
    direction = get_object_or_404(Direction, slug=direction_slug)
    services = Services.is_availability.filter(direction_id=direction.pk)

    data = {
        'title': f'Направление: {direction.name}',
        'menu': menu,
        'services': services,
        'dir_selected': direction.pk,  
    }
    return render(request, 'Voka/main_page.html', context=data)

def doctors(request):
    doctors = Doctors.objects.filter()
    return render(request, 'Voka/doctors.html',{'title' : 'Врачи', 'menu' : menu, 'doctors': doctors})

def show_docs(request, doc_slug):
    doc = get_object_or_404(Doctors, slug = doc_slug)
    services = doc.services.filter()
    data = {
        'title': f'Врач: {doc.name}',
        'menu': menu,
        'services': services,  
    }
    return render(request, 'Voka/doctors.html',context = data)

def about(request):
    return HttpResponse("О нас")

def price_list(request):
    return HttpResponse("Цены")

def news(request):
    return HttpResponse("Новости")

def login(request):
    return HttpResponse("Авторизация")

def contacts(request):
    return HttpResponse("Контакты")

def page_not_found(request, exception):
    return HttpResponseNotFound(render(request, 'Voka/page_not_found.html'))