from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
import uuid

from .models import CustomUser
from .forms import CustomUserCreationForm
from .forms import CustomSetPasswordForm

# Create your views here.

class HomeView(TemplateView):
    template_name = 'home.html'


class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:verify_email')

    def form_valid(self, form):
        user = form.save(commit=False)
        token = str(uuid.uuid4())
        user.email_verification_token = token
        user.token_created_at = timezone.now()

        subject = 'Verify your email address'
        current_site = get_current_site(self.request)
        verification_link = f'http://{current_site}/confirm_registration/{token}/'
        message = f'Click the following link to verify your email:\n{verification_link}'
        from_email = 'no-reply@awaisyasin.com'
        recipient_list = [form.cleaned_data['email']]
        send_mail(subject, message, from_email, recipient_list)
        user.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'There was a problem with your registration. Please try again.')
        return super().form_invalid(form)


class VerifyEmailView(TemplateView):
    template_name = 'accounts/verify_email.html'


class ConfirmRegistrationView(View):
    def validate_token(self, token):
        try:
            user = CustomUser.objects.get(email_verification_token=token)
            if user.is_verification_token_expired():
                return None
        except CustomUser.DoesNotExist:
            return None
        return user

    def get(self, request, token):
        user = self.validate_token(token)
        if user is None:
            return HttpResponse('<h1>Invalid or expired verification token.</h1>', content_type='text/html')
        form = CustomSetPasswordForm(user)
        return render(request, 'accounts/confirm_registration.html', {'form': form})

    def post(self, request, token):
        user = self.validate_token(token)
        if user is None:
            return HttpResponse('<h1>Invalid or expired verification token.</h1>', content_type='text/html')
        form = CustomSetPasswordForm(user, request.POST)
        if form.is_valid():
            user.is_email_verified = True
            user.email_verification_token = None
            user.token_created_at = None
            user.save()
            form.save()
            return redirect('accounts:home')
        else:
            return render(request, 'accounts/confirm_registration.html', {'form': form})