from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse_lazy
from .models.services import Services, Direction, Order
from .models.doctors import Doctors
from .models.appointment import Appointment
from .forms import AppointmentForm, RegistrationForm,ServicesForm
from django.views.generic.edit import CreateView,FormView
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


menu = [
    {'title': 'О центре', 'url_name': 'about'},
    {'title': 'Услуги', 'url_name': 'services'},
    {'title': 'Врачи', 'url_name': 'doctors'},
    {'title': 'Новости', 'url_name': 'news'},
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
    sale = services.filter(on_sale = Services.OnSale.SALEYES) 
    doctors = Doctors.objects.all().order_by('-experience')
    manager = doctors.filter(manager = Doctors.Managers.YES)

    return render(request, 'Voka/main_page.html', {
        'title': 'Главная страница',
        'menu': menu,
        'services': services,   
        'manager':manager,
        'sale':sale,
        'SALEYES': Services.OnSale.SALEYES,
        'doctors':doctors,
        'YES': Doctors.Managers.YES,
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


def services_create(request):
    if request.method == 'POST':
        form = ServicesForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            return redirect('services')
    else:
        form = ServicesForm()
    return render(request, 'Voka/services_form.html', {'form': form,'title':"Создание услуги",'menu':menu,})


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
    doctors = Doctors.objects.all().order_by('-experience')
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


@login_required
def appointment(request, service_id=None):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()

            service = appointment.services

            Order.objects.get_or_create(user=request.user, service=service)

            messages.success(request, f'Вы успешно записались на услугу "{service.title}"!')
            return redirect('profile')
    else:
        form = AppointmentForm()

    return render(request, "Voka/appointment.html", {
        'title': "Запись на приём",
        'menu': menu,
        'form': form,
    })




def news(request):
    return HttpResponse("Новости")

@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'Voka/profile.html', {
        'title': 'Профиль',
        'orders' : orders,
        'menu': menu,
    })

class Registration(FormView):
    form_class = RegistrationForm
    template_name = "registration/registration.html"
    success_url = reverse_lazy("main_page")

    def form_valid(self, form:RegistrationForm):
        form.save()
        return super().form_valid(form)


def page_not_found(request, exception):
    return render(request, 'Voka/page_not_found.html', status=404)