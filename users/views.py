from django.shortcuts import redirect
from rest_framework.decorators import api_view
from .models import User
from rest_framework.response import Response
from .serializers import ChangePasswordSerializer, PasswordResetConfirmSerializer, ResetPasswordSerializer, UserSerializer
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

from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.views import APIView

# Create your views here.
#----------------------------SOCIAL AUTH----------------------------------------------------------------------------

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
#===================================================================================================================

class UserRegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        # Check if the email already exists
        if User.objects.filter(email=request.data['email']).exists():
            return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(email=request.data['email'])
            serializer = UserSerializer(user)

            user_email = User.objects.get(email=user.email)
            tokens = RefreshToken.for_user(user_email).access_token
            # send email for user verification
            current_site = get_current_site(request).domain
            relative_link = reverse('email-verify')
            absurl = 'http://'+current_site+relative_link+"?token="+str(tokens)
            email_body = 'Hi '+user.first_name + \
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


#=============================== TEST VIEW =========================================================================


# @api_view(["GET"])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def testview(request):
#     return Response({"message":"test view"})
# class TestView(GenericAPIView):
#     authentication_classes = [SessionAuthentication, TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         return Response({"message": "test view"})

#==============================   LOGOUT VIEW ======================================================================
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
    
 #################################################################################################################   

@api_view(['POST'])
def reset_password_view(request):
    serializer = ResetPasswordSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        # Send a password reset email to the user
        return Response({'message': 'Password reset email sent'})
    return Response(serializer.errors, status=400)
###################################################################################################################


@api_view(['POST'])
def password_reset_confirm_view(request):
    serializer = PasswordResetConfirmSerializer(data=request.data)
    if serializer.is_valid():
        password = serializer.validated_data['password']
        confirm_password = serializer.validated_data['confirm_password']
        token = serializer.validated_data['token']
        uidb64 = serializer.validated_data['uidb64']
        try:
            uid = force_bytes(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise ValidationError({'uidb64': 'Invalid user ID'})

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise ValidationError({'token': 'Invalid token'})

        user.set_password(password)
        user.save()
        return Response({'message': 'Password reset successfully'})
    return Response(serializer.errors, status=400)

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








