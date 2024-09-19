from django.db import models

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=255)
    venue = models.CharField(max_length=255)
    date = models.DateTimeField()
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    ticketLink = models.URLField(max_length=1000)
    desc = models.TextField()
    # ticketPrice = models.DecimalField(max_digits=10, decimal_places=2)
    

    def __str__(self):
        return self.name