from django.urls import path

from .views import HomeView, RegisterView, VerifyEmailView, ConfirmRegistrationView

app_name = 'accounts'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify_email/', VerifyEmailView.as_view(), name='verify_email'),
    path('confirm_registration/<str:token>/', ConfirmRegistrationView.as_view(), name='confirm_registration'),
]
