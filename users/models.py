from django.db import models
from django.contrib.auth.models import User

# Create your models here.

from django.db import models

class Event(models.Model):
  name = models.CharField(max_length=255)
  description = models.TextField(null=True, blank=True)
  participants = models.ManyToManyField(User, blank=True)
  date = models.DateTimeField()
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name
  

class Submission(models.Model):
  event = models.ForeignKey(Event, on_delete=models.CASCADE)
  participant = models.ForeignKey(User, on_delete=models.CASCADE)
  submission_date = models.DateTimeField(auto_now_add=True)
  details = models.TextField(null=True, blank=True)

  def __str__(self):
    return str(self.event)+"---"+str(self.participant)
