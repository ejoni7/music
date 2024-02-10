from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'accounts'
urlpatterns = [
    path('login/', views.login, name='login'),
    # path('login_api/', obtain_auth_token, name='auth_token'),
    path('login_api/', views. LoginApi.as_view(), name='login_api'),
    path('logout_/', views.logout_, name='logout_'),
    path('logout_api/', views.LogoutApi.as_view(), name='logout_api'),
    path('register/', views.register, name='register'),
    path('register_api/', views.RegisterApi.as_view(), name='register_api'),
    path('phone_check/', views.phone_check, name='phone_check'),
    path('profile/', views.profile, name='profile'),
    path('profile_api/', views.ProfileApi.as_view(), name='profile_api'),
    path('rules/', views.Rules.as_view(), name='rules'),
    # path('ends/', views.Ends.as_view(), name='ends'),
    path('change_password/', views.change_password, name='change_password'),
    path('change_password_api/', views.ChangePassword.as_view(), name='change_password_api'),
    # path('forget_password/', views.ForgetPassword.as_view(), name='forget_password'),
    # path('password_reset_done/', views.ResetDone.as_view(), name='password_reset_done'),
    # path('confirm_password/<uidb64>/<token>/', views.ConfirmPassword.as_view(), name='confirm_password'),
    # path('confirm_done/', views.ConfirmDone.as_view(), name='confirm_done'),
    path('forget_password/', views.forget_password, name='forget_password'),
    path('forget_password_api/', views.ForgetPassword.as_view(), name='forget_password_api'),

]
