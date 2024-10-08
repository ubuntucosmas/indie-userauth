from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from .models import User
from rest_framework.response import Response
from .serializers import PasswordResetConfirmSerializer, ResetPasswordSerializer, UserSerializer
from rest_framework import status, response
from rest_framework.authtoken.models import Token 
from django.contrib.auth import authenticate, logout
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated



from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework import serializers
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from . import serializers, models
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from .utils import Util
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.renderers import TemplateHTMLRenderer

from django.http import HttpResponse, JsonResponse
from rest_framework import generics, status
from rest_framework.views import APIView

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
#----------------------------SOCIAL AUTH----------------------------------------------------------------------------
# def home(request):
#     return render(request, './users/login.html')

#===================================================================================================================
def successVerification(request):
    html_content ="""
    <html>
        <body>
            <h1>Welcome!</h1>
            <p>Email verification successful!.. click <a href="https://indiearts.art/login">here</a> to visit our website.</p>
        </body>
    </html>"""
    return HttpResponse(html_content)


#---------------------------------------USER REGISTER OR SIGNUP-----------------------------------------------------
@method_decorator(csrf_exempt, name='dispatch') 
class UserRegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


    def post(self, request, *args, **kwargs):
        # Check if the email already exists
        if User.objects.filter(email=request.data['email']).exists():
            return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(email=request.data['email'])
            
            serializer = UserSerializer(user)

            user_email = models.User.objects.get(email=user.email)
            tokens = RefreshToken.for_user(user_email).access_token
            
            # send email for user verification
            current_site = get_current_site(request).domain
            relative_link = reverse('email-verify')
            absurl = 'http://'+current_site+relative_link+"?token="+str(tokens)
            email_body = 'Hi '+user.firstName + \
                ' Use the link below to verify your email \n' + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Verify your email'}

            Util.send_email(data=data)

            return Response({'user_data': serializer.data, 'access_token': str(tokens)}, status=status.HTTP_201_CREATED)

        return Response({'error': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)

    

#-------------------------EMAIL VERIFICATION------------------------------------------------------------------------

from django.conf import settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class VerifyEmail(GenericAPIView):
    serializer_class = serializers.EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            print(payload)
            user = models.User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return redirect('https://indiearts.art/login')
        except jwt.ExpiredSignatureError as identifier:
            return response.Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return response.Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        


 
#=============================== LOGIN VIEW  =======================================================================

@method_decorator(csrf_exempt, name='dispatch') 
class UserLoginView(APIView):
    serializer_class = UserSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return Response({"detail": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            authenticate_user = authenticate(email=user.email, password=password)
            if authenticate_user is not None:
                serializer = UserSerializer(user)
                response_data = {
                    "user": serializer.data,
                }
                token, created = Token.objects.get_or_create(user=user)
                response_data['token'] = token.key
                return Response(response_data)
            else:
                return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({"detail": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#==============================   LOGOUT VIEW ======================================================================
@method_decorator(csrf_exempt, name='dispatch')
class UserLogoutView(APIView):
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()  # Delete the user's token
            logout(request)  # Log the user out
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    
 #----------------------------------------PASSWORDRESET------------------------------------------------------------   

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.forms import PasswordResetForm
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail

@api_view(['POST'])
def reset_password_view(request):
    # Serializer to validate the email field
    serializer = ResetPasswordSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        
        # Check if a user with the email exists
        associated_users = User.objects.filter(email=email)
        if associated_users.exists():
            for user in associated_users:
                # Generate a password reset token
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                # Create a password reset URL
                reset_url = f"{settings.FRONTEND_URL}/NewPassword/{uid}/{token}"
                
                # Prepare the email context
                context = {
                    'email': user.email,
                    'domain': settings.FRONTEND_URL,  # Your frontend domain
                    'site_name': 'INDIE',
                    'uid': uid,
                    'user': user,
                    'token': token,
                    'reset_url': reset_url,
                }
                
                # Render the email template with the context
                subject = "Password Reset Requested"
                email_template_name = "registration/password_reset_email.txt"  # You can also use HTML emails
                email_body = render_to_string(email_template_name, context)
                
                # Send the email
                send_mail(subject, email_body, settings.DEFAULT_FROM_EMAIL, [user.email])

            return Response({'message': 'Password reset email sent'}, status=200)
        
        return Response({'message': 'No user is associated with this email'}, status=400)

    return Response(serializer.errors, status=400)


# @api_view(['POST'])
# def reset_password_view(request):
#     serializer = ResetPasswordSerializer(data=request.data)
#     if serializer.is_valid():
#         email = serializer.validated_data['email']
#         # Send a password reset email to the user
#         return Response({'message': 'Password reset email sent'})
#     return Response(serializer.errors, status=400)
###################################################################################################################


class PasswordResetConfirmView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
        
        return Response({'message': 'Password reset failed', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

#################################################################################################

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def change_password_view(request):
#     serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
#     if serializer.is_valid():
#         old_password = serializer.validated_data['old_password']
#         new_password = serializer.validated_data['new_password']
#         request.user.set_password(new_password)
#         request.user.save()
#         return Response({'message': 'Password changed successfully'})
#     return Response(serializer.errors, status=400)

# from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
# from allauth.socialaccount.providers.oauth2.client import OAuth2Client
# from dj_rest_auth.registration.views import SocialLoginView

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# @method_decorator(csrf_exempt, name='dispatch')
# class GoogleLogin(SocialLoginView): # if you want to use Authorization Code Grant, use this
#     adapter_class = GoogleOAuth2Adapter
#     callback_url = 'http://127.0.0.1:8000/accounts/google/login/callback/'
#     client_class = OAuth2Client

# class GoogleLogin(SocialLoginView): # if you want to use Implicit Grant, use this
#     adapter_class = GoogleOAuth2Adapter


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
import requests
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


  # Get your custom user model

class GoogleLogin(APIView):
    def post(self, request):
        token = request.data.get('id_token')

        if not token:
            return Response({'error': 'No ID token provided'}, status=400)

        response = requests.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={token}")

        if response.status_code != 200:
            return Response({'error': 'Invalid token'}, status=400)

        user_info = response.json()
        email = user_info.get('email')
        first_name = user_info.get('given_name')
        last_name = user_info.get('family_name')

        user, created = get_user_model().objects.get_or_create(email=email)

        if created:
            user.firstName = first_name
            user.lastName = last_name
            user.is_active = True 
            user.is_verified = True
            user.save()
            # send_verification_email(user, request)

        if not user.is_active:
            return Response({'error': 'Email not verified. Please check your inbox.'}, status=403)

        refresh = RefreshToken.for_user(user)
        return JsonResponse({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

    


     
    
