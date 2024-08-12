# from django.contrib.auth.models import User
# from rest_framework.serializers import ModelSerializer
# from rest_framework.authtoken.models import Token 

# class UserSerializer(ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'password']

#     def save(self, **kwargs):
#         new_user = User.objects.create_user(
#             username=self.validated_data['username'],
#             email=self.validated_data['email'],
#             password=self.validated_data['password'],
#         )
#         new_user.save()
#         new_Token = Token.objects.create(user=new_user)


from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from .models import User


from django.utils.encoding import smart_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class UserSerializer(ModelSerializer):
    class Meta():
        model = User
        fields = '__all__'

    def save(self, **kwargs):
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise ValidationError({'email': 'Email address already exists'})

        new_user = User.objects.create_user(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            email=self.validated_data['email'],
            password=self.validated_data['password'],
        )
        new_user.save()
        new_Token = Token.objects.create(user=new_user)
        return new_user



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        if not self.context['request'].user.check_password(old_password):
            raise ValidationError({'old_password': 'Incorrect password'})

        if new_password != confirm_password:
            raise ValidationError({'confirm_password': 'Passwords do not match'})

        return data


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, data):
        email = data.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError({'email': 'Email address not found'})
        return data


class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    uidb64 = serializers.CharField(required=True)

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        token = data.get('token')
        uidb64 = data.get('uidb64')

        try:
            uid = force_bytes(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise ValidationError({'uidb64': 'Invalid user ID'})

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise ValidationError({'token': 'Invalid token'})

        if password != confirm_password:
            raise ValidationError({'confirm_password': 'Passwords do not match'})

        user.set_password(password)
        user.save()
        return data
        