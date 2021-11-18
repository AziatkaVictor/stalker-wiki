from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.
class Type(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Stalker(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Page(models.Model):
    name = models.CharField(max_length=70)
    content = RichTextField()
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)
    type = models.ForeignKey(Type, on_delete=models.PROTECT)
    stalker = models.ForeignKey(Stalker, on_delete=models.PROTECT)
    date_publish = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + ' | ' + str(self.author)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('article-detail', kwargs={'pk': self.pk})

class HistoryType(models.Model):
    name = models.CharField(max_length=128)
    descr = models.CharField(blank=True, null=True, max_length=128)

    def __str__(self):
        return self.name

class History(models.Model):
    type = models.ForeignKey(HistoryType, blank=True, null=True, on_delete=models.PROTECT)
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)
    info = models.ForeignKey(Page, blank=True, null=True, on_delete=models.SET_NULL)
    info_name = models.CharField(blank=True, null=True, max_length=70)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.info_name)