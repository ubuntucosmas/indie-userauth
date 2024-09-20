from django.db import models

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=255)
    venue = models.CharField(max_length=255)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    ticketLink = models.URLField(max_length=2000,blank=True, null=True)
    desc = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    # ticketPrice = models.DecimalField(max_digits=10, decimal_places=2)
    

    def __str__(self):
        return self.name