from django.contrib.auth.backends import BaseBackend
from .models import Developer

class DeveloperBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            developer = Developer.objects.get(email=email)
            if developer.check_password(password):  # Ensure password is hashed
                return developer
        except Developer.DoesNotExist:
            return None

    def get_user(self, developer_id):
        try:
            return Developer.objects.get(pk=developer_id)
        except Developer.DoesNotExist:
            return None