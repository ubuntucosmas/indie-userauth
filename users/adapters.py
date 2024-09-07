
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .models import User

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        # Ensure username is not required, since you're using email as the identifier
        user = super().save_user(request, user, form, commit=False)
        user.firstName = form.cleaned_data.get('firstName')
        user.lastName = form.cleaned_data.get('lastName')
        user.save()
        return user

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        # Override this method to map fields correctly
        user = sociallogin.user
        user.email = data.get('email', '')
        user.firstName = data.get('first_name', '')
        user.lastName = data.get('last_name', '')
        return user
