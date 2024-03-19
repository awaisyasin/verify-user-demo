from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, username=None, password=None, **kwargs):
        if password is None:
            return None

        UserModel = get_user_model()
        try:
            user_email = email or username
            if user_email is None:
                return None
            user_email = user_email.lower()
            user = UserModel.objects.get(email=user_email)
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None
