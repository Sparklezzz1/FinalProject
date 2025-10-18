from django.db import models
from .services import Services
from .doctors import Doctors
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', _('В ожидании')),
        ('confirmed', _('Подтверждено')),
        ('done', _('Выполнено')),
        ('canceled', _('Отменено')),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctors, on_delete=models.PROTECT)
    services = models.ForeignKey(Services, on_delete=models.PROTECT)
    patient_name = models.CharField(max_length=255,verbose_name=_('Имя пациента'))
    patient_surname = models.CharField(max_length=255,verbose_name=_('Фамилия пациента'))
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField(blank=True, null=True,verbose_name=_('Причина обследования'))
    phone = models.CharField(
        _("Номер телефона"), max_length=13,
        validators=[
            RegexValidator(
                regex=r'^\+375(?:25|29|33|44|17)\d{7}$',
                message=_("Введите корректный номер телефона")
            )
        ]
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        unique_together = ('doctor', 'date', 'time')
        verbose_name = _("Запись")
        verbose_name_plural = _("Записи")

    def __str__(self):
        return f"{self.services.title} у {self.doctor} для {self.user.username}"
