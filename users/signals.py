from core import settings
# from users.views import send_verification_email
from .models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.core.mail import EmailMessage
import os


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:  # Only send the email when a new user is created
        subject = 'Welcome to Our Site!'
        message = f'Hi {instance.firstName}, thank you for signing up at our site.INDIE is Art-Tech.We are a Private Art Crowdfunding Platform. We connect great Artists to Art lovers to fund their work, to the mutual benefit of both.Fund Art with us, get returns, and grow hidden gems around the world. '
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]


        # Create an EmailMessage object
        email = EmailMessage(
            subject,
            message,
            from_email,
            recipient_list
        )

        # Path to the PDF file you want to attach
        pdf_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', 'welcome.pdf')  # Ensure you place the PDF in this directory

        # Check if the file exists before attaching
        if os.path.exists(pdf_path):
            email.attach_file(pdf_path)
        
        email.send()


