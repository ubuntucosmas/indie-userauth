from django.urls import path
from . views import EventListView, eventCreate, eventRetrieve, MpesaCheckoutView



urlpatterns = [
    path('api/events', EventListView.as_view(), name='events'),
    path('api/event/create', eventCreate.as_view(), name='create'),
    path('api/event/retrieve/<int:pk>/', eventRetrieve.as_view(), name='retrieve'),

    path('api/mpesa/checkout/', MpesaCheckoutView, name='mpesa_checkout'),
  
]