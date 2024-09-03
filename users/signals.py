from core import settings
from .models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:  # Only send the email when a new user is created
        subject = 'Welcome to Our Site!'
        message = f'Hi {instance.firstName}, thank you for signing up at our site.INDIE is Art-Tech.We are a Private Art Crowdfunding Platform. We connect great Artists to Art lovers to fund their work, to the mutual benefit of both.Fund Art with us, get returns, and grow hidden gems around the world. '
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]
        
        send_mail(subject, message, from_email, recipient_list)