from django.urls import path
from .views import EventListCreateView

urlpatterns = [
    path('api/events/', EventListCreateView.as_view(), name='event_list_create'),
]
