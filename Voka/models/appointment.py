from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('new', _('Новая')),
        ('confirmed', _('Подтверждена')),
        ('canceled', _('Отменена')),
        ('done', _('Завершена')),
    ]

    user = models.ForeignKey(
        User, verbose_name=_("Пользователь"), 
        on_delete=models.SET_NULL, null=True, blank=True
    )

    doctor = models.ForeignKey(
        'Voka.Doctors', verbose_name=_("Врач"),
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name='appointments'
    )

    services = models.ForeignKey(
        'Voka.Services', verbose_name=_("Услуга"),
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name='appointments'
    )

    patient_name = models.CharField(_("Имя пациента"), max_length=255, db_index=True)
    patient_surname = models.CharField(_("Фамилия пациента"), max_length=255, db_index=True)

    date = models.DateField(_("Дата приёма"), db_index=True)
    time = models.TimeField(_("Время приёма"), db_index=True)

    reason = models.TextField(_("Причина визита"), blank=True, null=True)
    phone = models.CharField(
        _("Номер телефона"), max_length=13,
        validators=[
            RegexValidator(
                regex=r'^\+375(?:25|29|33|44|17)\d{7}$',
                message=_("Введите корректный номер телефона")
            )
        ]
    )

    status = models.CharField(
        _("Статус"), max_length=20,
        choices=STATUS_CHOICES, default='new'
    )

    class Meta:
        unique_together = ('doctor', 'date', 'time')
        ordering = ['-date', '-time']
        verbose_name = _("Форма записи на приём")
        verbose_name_plural = _("Формы записи на приём")

    def __str__(self):
        return f"{self.patient_surname} {self.patient_name} — {self.services} ({self.date} {self.time})"
