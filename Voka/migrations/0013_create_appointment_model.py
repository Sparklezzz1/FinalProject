from django.db import migrations, models
import django.core.validators
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
    ('Voka', '0012_doctors_alter_services_availability_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_name', models.CharField(db_index=True, max_length=255, verbose_name='Имя пациента')),
                ('patient_surname', models.CharField(db_index=True, max_length=255, verbose_name='Фамилия пациента')),
                ('date', models.DateField(db_index=True, verbose_name='Дата приема')),
                ('time', models.TimeField(db_index=True, verbose_name='Время приёма')),
                ('reason', models.TextField(blank=True, null=True, verbose_name='Причина визита')),
                ('status', models.CharField(choices=[('new', 'Новая'), ('confirmed', 'Подтверждена'), ('canceled', 'Отменена'), ('done', 'Завершена')], default='new', max_length=20)),
                ('phone', models.CharField(max_length=13, validators=[django.core.validators.RegexValidator(message='Введите корректный номер телефона', regex='^\\+375(?:25|29|33|44|17)\\d{7}$')], verbose_name='Номер телефона')),
                ('services', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='services_appointments', to='Voka.services', verbose_name='Услуга')),
            ],
            options={
                'ordering': ['-date', '-time'],
                'unique_together': {('services', 'date', 'time')},
            },
        ),
    ]
