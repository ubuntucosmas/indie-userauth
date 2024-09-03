from django.urls import re_path
from . import views



urlpatterns = [
    re_path('login', views.UserLoginView.as_view(), name='login'),
    re_path('logout', views.UserLogoutView.as_view(), name='logout'),
    re_path('signup', views.UserRegisterView.as_view(), name='signup'),
    re_path('email-verify/', views.VerifyEmail.as_view(), name="email-verify"),
    re_path('redirect/', views.successVerification, name="redirect"),
    # re_path('test', views.TestView.as_view(), name='test'),
    re_path('reset', views.reset_password_view, name='reset'),
    re_path('resetconfirm', views.password_reset_confirm_view, name='resetconfirm'),
    # re_path('changepassword', views.change_password_view, name='changepassword'),
    


]