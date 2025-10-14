from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

class News(models.Model):
    title = models.CharField(verbose_name=_("Название новости"), max_length=250)
    date_create = models.DateField(verbose_name=_("Дата публикации"), auto_now_add=True)
    content = models.CharField(verbose_name=_("Контент новости"), max_length=1500)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, null=True)
    image = models.ImageField(
        upload_to='news/',  
        null=True,              
        blank=True,             
        default='news/default.jpg',  
    )

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'news_slug' : self.slug})
    
    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
