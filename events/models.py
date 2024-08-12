from django.db import models
from django.contrib.auth.models import User

from core.settings import AUTH_USER_MODEL

# Create your models here.

class Event(models.Model):
  name = models.CharField(max_length=255)
  description = models.TextField(null=True, blank=True)
  owner = models.ManyToManyField(AUTH_USER_MODEL, blank=True)
  event_poster = models.ImageField(null=True, blank=True,upload_to='images/')
  event_venue = models.CharField(max_length=100)
  date = models.DateTimeField()
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)


  def __str__(self):
    return self.name

