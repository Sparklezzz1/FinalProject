from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.template.loader import render_to_string

def main_page(request):
    # t = render_to_string('Voka/main_page.html')
    # return HttpResponse(t)
    return render(request,'Voka/main_page.html')

def services(request):
    return render(request, 'Voka/services.html')

def services_by_id(request, serv_id):
    return HttpResponse(f"<h1>Наши услуги</h1><p>id:{serv_id}</p>")

def services_by_slug(request, serv_slug):
    return HttpResponse(f"<h1>Наши услуги</h1><p>slug:{serv_slug}</p>")

def page_not_found(request, exception):
    return HttpResponseNotFound(render(request, 'Voka/page_not_found.html'))