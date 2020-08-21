from django.conf import settings
from django.db import models
from django.utils import timezone
import threading


class Articolo(models.Model):
     author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
     title = models.CharField(max_length=200)
     text = models.TextField()
     created_date = models.DateTimeField(default=timezone.now)
     published_date = models.DateTimeField(blank=True, null=True)

     def publish(self):
         self.published_date = timezone.now()
         self.save()

     def __str__(self):
         return self.title


class Simple_str(models.Model):
    key = models.CharField(max_length=200)


class ThreadTask(models.Model):
    task = models.CharField(max_length=30, blank=True, null=True)
    is_done = models.BooleanField(blank=False,default=False)
