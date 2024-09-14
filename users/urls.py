from django.urls import re_path
from . import views



urlpatterns = [
    re_path('dj-rest-auth/google/', views.GoogleLogin.as_view(), name='google_login'),
    # re_path('home', views.home, name='home'),
    re_path('login', views.UserLoginView.as_view(), name='login'),
    re_path('logout', views.UserLogoutView.as_view(), name='logout'),
    re_path('signup', views.UserRegisterView.as_view(), name='signup'),
    re_path('email-verify/', views.VerifyEmail.as_view(), name="email-verify"),
    re_path('redirect/', views.successVerification, name="redirect"),
    re_path('resetpassword', views.reset_password_view, name='resetpassword'),
    re_path('resetconfirm', views.PasswordResetConfirmView.as_view(), name='resetconfirm'),
    # re_path('changepassword', views.change_password_view, name='changepassword'),
    
    


]