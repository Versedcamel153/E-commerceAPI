from django.db import models
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from rest_framework_api_key.models import AbstractAPIKey, BaseAPIKeyManager
import secrets

class DeveloperManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        """
        Create and save a Developer with the given username, email, and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user_model = get_user_model()
        developer = user_model(username=username, email=email, **extra_fields)
        developer.set_password(password)
        developer.save(using=self._db)
        return developer

    def create_superuser(self, email, password=None, ** extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        return self.create_user(username='admin', email=email, password=password, **extra_fields)
    
class Developer(AbstractBaseUser):
    """
    Model for the developer user.
    """
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = DeveloperManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        """
        String representation of the developer.
        """
        return self.username  # Return the developer's username
    
    def has_perm(self, perm, obj=None):
        """
        Does the user have a specific permission?
        """
        return True

    def has_module_perms(self, app_label):
        """
        Does the user have permissions to view the app `app_label`?
        """
        return True

class DeveloperAPIKeyManager(BaseAPIKeyManager):
    pass

class DeveloperAPIKey(AbstractAPIKey):
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, related_name='api_key')

    objects = DeveloperAPIKeyManager()