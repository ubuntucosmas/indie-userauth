from django.contrib import admin
from .models import Event, Organizer, Venue,Ticket, TicketCategory, Order, Payment ,MpesaTransaction

# Register your models here.


admin.site.register(Organizer)
admin.site.register(Venue)
admin.site.register(Event)
admin.site.register(TicketCategory)
admin.site.register(Order)
admin.site.register(Ticket)
admin.site.register(Payment)
admin.site.register(MpesaTransaction)