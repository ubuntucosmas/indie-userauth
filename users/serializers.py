from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from .models import User


from django.utils.encoding import smart_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator


#=====================================USERSIGNUP SERIALIZER=========================================================

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only =True)
    firstName = serializers.CharField()
    lastName = serializers.CharField()
    # tokens = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'firstName', 'lastName', 'email', 'password', 'is_active' ]
    
    # def validate_password(self, value):
    #     if len(value) < 8:
    #         raise ValidationError("Password must be at least 8 characters long.")
    #     return value
    
    def save(self, **kwargs):
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise ValidationError({'email': 'Email address already exists'})

        new_user = User.objects.create_user(
            firstName=self.validated_data['firstName'],
            lastName=self.validated_data['lastName'],
            email=self.validated_data['email'],
            password=self.validated_data['password'],
        )
        new_user.save()
        new_Token = Token.objects.create(user=new_user)
        return new_user
    

#=====================================EMAIL VERIFICATION SERIALIZER=================================================
class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)
    class Meta:
        model = User
        fields = ['token']




#===================================================================================================================
# class ChangePasswordSerializer(serializers.Serializer):
#     old_password = serializers.CharField(required=True)
#     new_password = serializers.CharField(required=True)
#     confirm_password = serializers.CharField(required=True)

#     def validate(self, data):
#         old_password = data.get('old_password')
#         new_password = data.get('new_password')
#         confirm_password = data.get('confirm_password')

#         if not self.context['request'].user.check_password(old_password):
#             raise ValidationError({'old_password': 'Incorrect password'})

#         if new_password != confirm_password:
#             raise ValidationError({'confirm_password': 'Passwords do not match'})

#         return data

#===================================================================================================================
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, data):
        email = data.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError({'email': 'Email address not found'})
        return data

#===================================================================================================================
class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, data):
        uid = data.get('uid')
        token = data.get('token')
        new_password = data.get('new_password')

        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("Invalid user.")

        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError("Invalid or expired token.")

        return {
            'user': user,
            'new_password': new_password
        }

    def save(self):
        user = self.validated_data['user']
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        return user
        