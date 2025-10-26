from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _ 
from .models.services import Services, Direction
from .models.doctors import Doctors
from .models.appointment import Appointment
from .models.news import News
from .forms import AppointmentForm, RegistrationForm, ServicesForm
from django.views.decorators.http import require_POST

def get_menu():
    return [
        {'title': _('Услуги'), 'url_name': 'services'},
        {'title': _('Врачи'), 'url_name': 'doctors'},
        {'title': _('Новости'), 'url_name': 'news'},
        {'title': _('Запись на прием'), 'url_name': 'appointment'},
    ]

def get_filtered_services(doc_slug=None, dir_slug=None, sale_param=None):
    services = Services.objects.filter(availability=Services.Status.PUBLISHED)

    selected_doc = None
    selected_dir = None

    if doc_slug:
        selected_doc = get_object_or_404(Doctors, slug=doc_slug)
        services = services.filter(doctors=selected_doc)

    if dir_slug:
        selected_dir = get_object_or_404(Direction, slug=dir_slug)
        services = services.filter(direction=selected_dir)

    if sale_param == '1':  
        services = services.filter(on_sale=Services.OnSale.SALEYES)
    
    return services, selected_doc, selected_dir


def main_page(request):
    services, selected_doc, selected_dir  = get_filtered_services()
    
    doctors = Doctors.objects.all().order_by('-experience')
    news = News.objects.all()

    sale = services.filter(on_sale = Services.OnSale.SALEYES) 
    manager = doctors.filter(manager = Doctors.Managers.YES)

    sale_paginator = Paginator(sale,3)
    sale_page =request.GET.get('sale_page')
    sale_page_obj = sale_paginator.get_page(sale_page)


    doctor_paginator = Paginator(manager,3)
    doctor_page =request.GET.get('doctor_page')
    doctor_page_obj = doctor_paginator.get_page(doctor_page)

    news_paginator = Paginator(news,2)
    news_page = request.GET.get('news_page')
    news_page_obj = news_paginator.get_page(news_page)

    return render(request, 'Voka/main_page.html', {
        'title': _('Главная страница'),
        'menu': get_menu,
        'services': services,   
        'manager':manager,
        'SALEYES': Services.OnSale.SALEYES,
        'YES': Doctors.Managers.YES,
        'sale_page_obj':sale_page_obj,
        'doctor_page_obj':doctor_page_obj,
        'news_page_obj':news_page_obj, 
    })

def services(request):
    doc_slug = request.GET.get('doctor')
    dir_slug = request.GET.get('directions')
    sale_param = request.GET.get('sale')


    services, selected_doc, selected_dir = get_filtered_services(doc_slug, dir_slug,sale_param)
    return render(request, 'Voka/services.html', {
        'title': _('Услуги'),
        'menu': get_menu,
        'services': services,
        'selected_doc': selected_doc,
        'selected_dir': selected_dir,
        'sale_param':sale_param,
    })


def services_create(request):
    if request.method == 'POST':
        form = ServicesForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            return redirect('services')
    else:
        form = ServicesForm()
    return render(request, 'Voka/services_form.html', {'form': form,'title':"Создание услуги",'menu':get_menu,})


def service_delete(request, pk):
    service = get_object_or_404(Services, pk=pk)
    
    if request.method == "POST":
        service.delete()
        messages.success(request, f'Услуга "{service.title}" успешно удалена.')
        return redirect('services')

    return render(request, 'Voka/services_del.html', {'service': service})

def service_edit(request, service_id):
    service = get_object_or_404(Services, id=service_id)
    
    if request.method == 'POST':
        form = ServicesForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('services')  
    else:
        form = ServicesForm(instance=service)
    
    return render(request, 'VOka/services_edit.html', {'form': form, 'service': service})


def show_serv(request, serv_slug):
    serv = get_object_or_404(Services, slug=serv_slug)
    
    return render(request, 'Voka/serv.html', {
        'title': serv.title,
        'menu': get_menu,
        'serv': serv,
    })


def doctors(request):
    doctors = Doctors.objects.all().order_by('-experience')
    return render(request, 'Voka/doctors.html', {
        'title': _('Врачи'),
        'menu': get_menu,
        'doctors': doctors,
    })


def show_docs(request, doc_slug):
    doc = get_object_or_404(Doctors, slug=doc_slug)
    return render(request, 'Voka/doc.html', {
        'title': f'{doc.surname} {doc.name} {doc.patronymic}',
        'menu': get_menu,
        'doc': doc,
    })

@login_required
def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, user=request.user)
    if request.method == "POST":
        appointment.delete() 
        return redirect("profile")  


@login_required
def appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()

            service = appointment.services
            doctor = appointment.doctor

            if hasattr(request.user, 'profile'):
                request.user.profile.appointments.add(appointment)

            if hasattr(doctor, 'profile'):
                doctor.profile.appointments.add(appointment)

            messages.success(
                request, 
                f'Вы успешно записались на услугу "{service.title}" у врача "{doctor}"!'
            )
            return redirect('profile')
    else:
        form = AppointmentForm()

    return render(request, "Voka/appointment.html", {
        'title': _("Запись на приём"),
        'menu': get_menu,
        'form': form,
    })

@login_required
@require_POST
def appointment_update_status(request, pk):
    if not request.user.groups.filter(name='Doctors').exists():
        return redirect('profile')

    appointment = get_object_or_404(Appointment, pk=pk)
    doctor = getattr(appointment, 'doctor', None)

    if doctor and doctor.user == request.user:
        new_status = request.POST.get('status')
        if new_status in dict(Appointment.STATUS_CHOICES):
            appointment.status = new_status
            appointment.save()
            messages.success(request, _("Статус приёма обновлён"))
    return redirect('profile')


def news(request):
    news = News.objects.all()
    return render(request, 'Voka/news.html',{
        'title':"Новости",
        "menu":get_menu,
        "news":news,
    })

def news_detail(request,news_slug):
    news = get_object_or_404(News, slug=news_slug)
    return render(request, 'Voka/news_detail.html',{
        'title':"Новости",
        "menu":get_menu,
        "news":news,
    })

@login_required
def profile(request):
    appointment_user = Appointment.objects.filter(user=request.user)
    appointment_doctor = None

    if request.user.groups.filter(name='Doctors').exists():
        appointment_doctor = Appointment.objects.filter(doctor__user_id=request.user.id)

    return render(request, 'Voka/profile.html', {
        'title': 'Профиль',
        'appointment_user': appointment_user,
        'appointment_doctor': appointment_doctor,
        'menu': get_menu,
    })

class Registration(FormView):
    form_class = RegistrationForm
    template_name = "registration/registration.html"
    success_url = reverse_lazy("main_page")

    def form_valid(self, form:RegistrationForm):
        form.save()
        return super().form_valid(form)

def toggle_theme(request):
    darkmode = request.session.get('darkmode', False)
    request.session['darkmode'] = not darkmode
    return redirect(request.META.get('HTTP_REFERER', '/'))

def page_not_found(request, exception):
    return render(request, 'Voka/page_not_found.html', status=404)