from core import settings
from .models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
from email.mime.image import MIMEImage  # Import for embedding images
import os

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:  # Only send the email when a new user is created
        subject = 'Welcome to INDIE!'
        
        # HTML message with embedded image at the bottom
        html_message = (f'<p>Hi there!'
                        '<p>Invest in Art.</p>'
                        '<p>Projected: 10 - 12% Return on Investment within a month.</p>'
                        'More info attached.</p>'
                        '<p>INDIE is Art, and Art is Popping.</p>'
                        '<p>Best regards,<br>INDIE Team</p>'
                        '<p><img src="cid:infor" alt="Welcome Image" style="width:300px;height:auto;"></p>')  # Embedding the image

        # Fallback plain-text version for email clients that don't support HTML
        plain_message = (f"Hi there! Invest in Art. Projected: 10 - 12% Return on Investment within a month.\n"
                         "More info attached.\n\n"
                         "INDIE is Art, and Art is Popping.\n\n"
                         "Best regards,\nINDIE Team")

        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]

        # Create an EmailMessage object
        email = EmailMessage(
            subject,
            plain_message,  # Plain-text fallback message
            from_email,
            recipient_list
        )

        # Set the email content to HTML
        email.content_subtype = 'html'

        # Path to the image file to embed in the email body
        image_path = os.path.join(settings.MEDIA_ROOT, 'images', 'infor.png')  # Adjust this path as needed

        # Path to the PDF file to attach
        pdf_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', 'welcome.pdf')

        # Embed the image in the email if it exists
        if os.path.exists(image_path):
            with open(image_path, 'rb') as img:
                mime_image = MIMEImage(img.read())
                mime_image.add_header('Content-ID', '<infor>')  # Set Content-ID to use in the HTML
                email.attach(mime_image)

        # Attach the PDF file if it exists
        if os.path.exists(pdf_path):
            email.attach_file(pdf_path)

        # Send the email
        email.send()











# from core import settings
# # from users.views import send_verification_email
# from .models import User

# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.core.mail import send_mail
# from django.core.mail import EmailMessage
# import os


# @receiver(post_save, sender=User)
# def send_welcome_email(sender, instance, created, **kwargs):
#     if created:  # Only send the email when a new user is created
#         subject = 'Welcome to Our Site!'
#         message = f'Hi {instance.firstName}, Hi there! Invest in Art. Projected: 10 - 12% Return on Investment within a month. More info attached. 
#         INDIE is Art, and Art is Popping.'
#         from_email = settings.DEFAULT_FROM_EMAIL
#         recipient_list = [instance.email]


#         # Create an EmailMessage object
#         email = EmailMessage(
#             subject,
#             message,
#             from_email,
#             recipient_list
#         )

#          # Path to the image file you want to attach
#         image_path = os.path.join(settings.MEDIA_ROOT, 'images', 'welcome_image.jpg')  # Adjust this as needed

#         # Path to the PDF file you want to attach
#         pdf_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', 'welcome.pdf')  # Ensure you place the PDF in this directory

#         # Check if the file exists before attaching
        
#         if os.path.exists(image_path):
#             email.attach_file(image_path)

#         if os.path.exists(pdf_path):
#             email.attach_file(pdf_path)
        
#         email.send()


