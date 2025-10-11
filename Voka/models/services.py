from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from slugify import slugify
from django.contrib.auth.models import User

class Services(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, "Услуга не доступна"
        PUBLISHED = 1, "Услуга доступна"

    class OnSale(models.IntegerChoices):
        SALENO = 0, "Скидки нет"
        SALEYES = 1, "Скидка"

    title = models.CharField(verbose_name="Услуга", max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    content = models.TextField(verbose_name="Описание",blank=True)
    price = models.FloatField(verbose_name="Стоимость",null=True, blank=True)
    time_create=models.DateTimeField(verbose_name="Время создания",auto_now_add=True)
    time_update=models.DateTimeField(verbose_name="Время изменения",auto_now=True)
    availability = models.IntegerField(verbose_name="Доступность услуги",choices=Status.choices, default=Status.PUBLISHED)
    direction = models.ForeignKey('Direction',verbose_name="Направление", on_delete=models.PROTECT)
    doctors = models.ManyToManyField('Voka.Doctors',verbose_name="Время создания", blank=True,related_name="services")
    on_sale = models.IntegerField(verbose_name="На акции",choices=OnSale.choices, default=OnSale.SALENO)
    sale_price = models.FloatField(verbose_name="Размер скидки",null=True, blank=True)
    image = models.ImageField(
        upload_to='services/',  
        null=True,              
        blank=True,             
        default='services/default.jpg',  
    )

    objects = models.Manager()

    def final_price(self):
        if self.sale_price:
            return self.price - self.sale_price
        return self.price

    def save(self, *args, **kwargs):
        if not self.slug: 
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('serv', kwargs={'serv_slug' : self.slug})
    
    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

class Direction(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255,unique=True,db_index=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Направление"
        verbose_name_plural = "Направления"
    
class Order(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.PROTECT)
    service = models.ForeignKey(Services, verbose_name="Услуга", on_delete=models.PROTECT)
    
    def __str__(self):
        return f"{self.user.username} - {self.service.title}"
    
    class Meta:
        verbose_name = "Запись на прием"
        verbose_name_plural = "Записи на прием"

    

