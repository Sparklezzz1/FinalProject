from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseNotFound
from .models.services import Services
from .models.services import Direction
from .models.doctors import Doctors
from .models.appointment import Appointment
from .forms import AppointmentForm

menu = [
    {'title': 'О центре', 'url_name': 'about'},
    {'title': 'Услуги', 'url_name': 'services'},
    {'title': 'Цены', 'url_name': 'price_list'},
    {'title': 'Врачи', 'url_name': 'doctors'},
    {'title': 'Новости', 'url_name': 'news'},
    {'title': 'Контакты', 'url_name': 'contacts'},
    {'title': 'Авторизация', 'url_name': 'login'},
    {'title': 'Запись на прием', 'url_name': 'appointment'},
]


def get_filtered_services(doc_slug=None, dir_slug=None):
    services = Services.objects.filter(availability=Services.Status.PUBLISHED)

    selected_doc = None
    selected_dir = None

    if doc_slug:
        selected_doc = get_object_or_404(Doctors, slug=doc_slug)
        services = services.filter(doctors=selected_doc)

    if dir_slug:
        selected_dir = get_object_or_404(Direction, slug=dir_slug)
        services = services.filter(direction=selected_dir)

    return services, selected_doc, selected_dir


def main_page(request):
    services, _, _ = get_filtered_services()
    return render(request, 'Voka/main_page.html', {
        'title': 'Главная страница',
        'menu': menu,
        'services': services,
    })


def services(request):
    doc_slug = request.GET.get('doctor')
    dir_slug = request.GET.get('directions')

    services, selected_doc, selected_dir = get_filtered_services(doc_slug, dir_slug)
    return render(request, 'Voka/services.html', {
        'title': 'Услуги',
        'menu': menu,
        'services': services,
        'selected_doc': selected_doc,
        'selected_dir': selected_dir,
    })


def show_serv(request, serv_slug):
    serv = get_object_or_404(Services, slug=serv_slug)
    return render(request, 'Voka/serv.html', {
        'title': serv.title,
        'menu': menu,
        'serv': serv,
    })


def filter_direction(request, direction_slug):
    direction = get_object_or_404(Direction, slug=direction_slug)
    services = Services.objects.filter(
        availability=Services.Status.PUBLISHED,
        direction=direction
    )
    return render(request, 'Voka/main_page.html', {
        'title': f'Направление: {direction.name}',
        'menu': menu,
        'services': services,
        'dir_selected': direction.pk,
    })


def doctors(request):
    doctors = Doctors.objects.all()
    return render(request, 'Voka/doctors.html', {
        'title': 'Врачи',
        'menu': menu,
        'doctors': doctors,
    })


def show_docs(request, doc_slug):
    doc = get_object_or_404(Doctors, slug=doc_slug)
    return render(request, 'Voka/doc.html', {
        'title': f'{doc.surname} {doc.name} {doc.patronymic}',
        'menu': menu,
        'doc': doc,
    })


def about(request):
    return render(request, 'Voka/about.html', {
        'title': 'О нас',
        'menu': menu,
    })

def appointment(request):
    form = AppointmentForm()
    return render(request, "Voka/appointment.html",{'title':"Запись на прием",'menu':menu,'form':form})

def price_list(request):
    return HttpResponse("Цены")


def news(request):
    return HttpResponse("Новости")


def login(request):
    return HttpResponse("Авторизация")


def contacts(request):
    return HttpResponse("Контакты")


def page_not_found(request, exception):
    return render(request, 'Voka/page_not_found.html', status=404)