from django.db import models

from core.settings import AUTH_USER_MODEL
import uuid

# Create your models here.



class Organizer(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.organization_name


class Venue(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name}, {self.city}"


class Event(models.Model):
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE, related_name='events')
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    

    def __str__(self):
        return self.title


class TicketCategory(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='ticket_categories')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.event.title}"


class Order(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} by {self.user.email}"


class Ticket(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='tickets')
    ticket_category = models.ForeignKey(TicketCategory, on_delete=models.CASCADE)
    ticket_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    purchaser_name = models.CharField(max_length=255)
    purchaser_email = models.EmailField()
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"Ticket {self.ticket_uuid} for {self.ticket_category.name}"


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, choices=(
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('mpesa', 'Mpesa'),
    ))
    payment_status = models.CharField(max_length=20, choices=(
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ), default='pending')
    transaction_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Payment for Order {self.order.id} - {self.payment_status}"
    



#------------------------------mpesa payment model------------------------------------------------------------
    


class MpesaTransaction(models.Model):
    transaction_type = models.CharField(max_length=50)
    trans_id = models.CharField(max_length=50, unique=True)
    trans_time = models.DateTimeField()
    trans_amount = models.DecimalField(max_digits=10, decimal_places=2)
    business_shortcode = models.CharField(max_length=20)
    bill_ref_number = models.CharField(max_length=100)
    invoice_number = models.CharField(max_length=100, blank=True, null=True)
    third_party_trans_id = models.CharField(max_length=100, blank=True, null=True)
    msisdn = models.CharField(max_length=15)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.trans_id} - {self.first_name} {self.last_name}"


