from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from .serializers import EventSerializer
from .models import Event
from rest_framework.generics import CreateAPIView,RetrieveAPIView, GenericAPIView

class EventListView(GenericAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get(self, request, *args, **kwargs):
        events = self.get_queryset()
        serializer = self.get_serializer(events, many=True)
        return JsonResponse(serializer.data)

class eventCreate(CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
class eventRetrieve(RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


import requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.views import View
from django.http import JsonResponse
from rest_framework import status

# class MpesaCheckoutView(View):
    # def post(self, request, *args, **kwargs):
def MpesaCheckoutView(request):

    return render(request, './events/checkout.html')
        # phone_number = request.POST.get('phone_number')
        # amount = request.POST.get('amount')

    #     if not phone_number or not amount:
    #         return JsonResponse({'error': 'Phone number and amount are required'}, status=status.HTTP_400_BAD_REQUEST)

    #     # Make the STK Push request to M-Pesa
    #     access_token = self.get_access_token()
    #     if not access_token:
    #         return JsonResponse({'error': 'Unable to authenticate with M-Pesa'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #     response = self.initiate_stk_push(phone_number, amount, access_token)
    #     if response.get('ResponseCode') == '0':
    #         return JsonResponse({'message': 'Payment initiated successfully. Please check your phone to complete the payment.'})
    #     else:
    #         return JsonResponse({'error': 'Failed to initiate payment', 'details': response}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def get_access_token(self):
    #     """Get the access token from Safaricom Daraja API"""
    #     consumer_key = settings.MPESA_CONSUMER_KEY
    #     consumer_secret = settings.MPESA_CONSUMER_SECRET
    #     api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    #     response = requests.get(api_url, auth=(consumer_key, consumer_secret))
    #     if response.status_code == 200:
    #         return response.json().get('access_token')
    #     return None

    # def initiate_stk_push(self, phone_number, amount, access_token):
    #     """Initiate the STK Push for M-Pesa payment"""
    #     api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    #     headers = {
    #         'Authorization': f'Bearer {access_token}',
    #         'Content-Type': 'application/json',
    #     }
    #     payload = {
    #         'BusinessShortCode': settings.MPESA_SHORTCODE,
    #         'Password': self.get_encoded_password(),
    #         'Timestamp': self.get_timestamp(),
    #         'TransactionType': 'CustomerPayBillOnline',
    #         'Amount': amount,
    #         'PartyA': phone_number,
    #         'PartyB': settings.MPESA_SHORTCODE,
    #         'PhoneNumber': phone_number,
    #         'CallBackURL': settings.MPESA_CALLBACK_URL,
    #         'AccountReference': 'Ticket Payment',
    #         'TransactionDesc': 'Payment for Event Ticket',
    #     }

    #     response = requests.post(api_url, json=payload, headers=headers)
    #     return response.json()

    # def get_encoded_password(self):
    #     """Generate the encoded password for M-Pesa"""
    #     from base64 import b64encode
    #     from datetime import datetime

    #     data_to_encode = settings.MPESA_SHORTCODE + settings.MPESA_PASSKEY + self.get_timestamp()
    #     encoded_string = b64encode(data_to_encode.encode())
    #     return encoded_string.decode('utf-8')

    # def get_timestamp(self):
    #     """Get the timestamp in the format YYYYMMDDHHMMSS"""
    #     from datetime import datetime
    #     return datetime.now().strftime('%Y%m%d%H%M%S')

