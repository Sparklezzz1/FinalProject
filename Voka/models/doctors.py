from Voka import models
from django.db import models
from django.urls import reverse


class Doctors(models.Model):
    class Managers(models.IntegerChoices):
        NO = 0, "Не входит в руководство"
        YES = 1, "Входит в руководство"

    name = models.CharField(verbose_name="Имя",max_length=255,db_index=True)
    surname = models.CharField(verbose_name="Фамилия",max_length=255)
    patronymic = models.CharField(verbose_name="Отчество",max_length=255)
    job_title = models.CharField(verbose_name="Должность",max_length=255,null=True,blank=True)
    experience = models.IntegerField(verbose_name="Стаж работы", default=0,)
    slug = models.SlugField(max_length=255,unique=True,db_index=True)
    manager = models.IntegerField(verbose_name="Руководство", choices=Managers.choices, default=Managers.NO)
    image = models.ImageField(
        upload_to='doctors/',  
        null=True,              
        blank=True,             
        default='doctors/default.jpg',  
    )
    

    def __str__(self):
         return f"{self.surname} {self.name} {self.patronymic}"
         
    def get_absolute_url(self):
        return reverse('doc', kwargs={'doc_slug' : self.slug})