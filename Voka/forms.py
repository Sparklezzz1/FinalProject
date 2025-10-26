from django import forms
from django.contrib.auth.models import User
from Voka.models.doctors import Doctors 
from .models.appointment import Appointment
from .models.services import Services
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class AppointmentForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label=_("Дата приёма")
    )

    TIME_CHOICES = [(f"{h:02}:00", f"{h}:00") for h in range(10, 19)]
    time = forms.TimeField(
        widget=forms.Select(choices=TIME_CHOICES, attrs={'class': 'form-control'}),
        label=_("Время приёма")
    )

    class Meta:
        model = Appointment
        fields = ['doctor', 'patient_name', 'patient_surname', 'services', 'date', 'time', 'reason', 'phone']
        widgets = {
            'doctor': forms.Select(attrs={'class': 'form-select'}),
            'services': forms.Select(attrs={'class': 'form-select'}),
            'patient_name': forms.TextInput(attrs={'class': 'form-control'}),
            'patient_surname': forms.TextInput(attrs={'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_date(self):
        date = self.cleaned_data.get('date')
        today = timezone.localdate()

        if date < today:
            self.add_error('date', _("Нельзя выбрать прошедшую дату."))
        elif date.weekday() in (5, 6):
            self.add_error('date', _("Нельзя записаться на выходные."))

        return date



class ServicesForm(forms.ModelForm):
    doctors = forms.ModelMultipleChoiceField(
        queryset=Doctors.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
        required=True,
        label=_("Врачи")
    )

    class Meta:
        model = Services
        fields = ['title', 'content', 'price', 'direction', 'doctors', 'on_sale', 'sale_price', 'image', 'availability']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class RegistrationForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput)

    def save(self):
        same_name_users = User.objects.filter(username=self.cleaned_data["username"]).exists()
        if not same_name_users and self.cleaned_data["password"] == self.cleaned_data["repeat_password"]:
            user = User(username=self.cleaned_data["username"])
            user.set_password(self.cleaned_data["password"])  
            user.save()
            return user
        return None
