from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    """
    Custom manager for the CustomUser model to handle user creation.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError(_('The Email field must be set'))  # Ensure email is provided
        email = self.normalize_email(email)  # Normalize the email
        user = self.model(email=email, **extra_fields)  # Create user instance
        user.set_password(password)  # Set the user's password
        user.save(using=self._db)  # Save the user to the database
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.
        """
        extra_fields.setdefault('is_staff', True)  # Ensure the superuser is staff
        extra_fields.setdefault('is_superuser', True)  # Ensure the superuser has superuser permissions

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))  # Raise error if not staff
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))  # Raise error if not superuser

        return self.create_user(email, password, **extra_fields)  # Create the user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that supports using email as the username.
    """
    email = models.EmailField(_('email address'), unique=True)  # User's email address
    username = models.CharField(max_length=150, blank=True, null=True, unique=True)  # Optional username
    is_staff = models.BooleanField(default=False)  # Is the user a staff member?
    is_active = models.BooleanField(default=True)  # Is the user active?
    date_joined = models.DateTimeField(auto_now_add=True)  # Date when the user joined

    objects = CustomUserManager()  # Use the custom user manager

    USERNAME_FIELD = 'email'  # Define the field to be used as the username
    REQUIRED_FIELDS = []  # No required fields for creating a user

    def __str__(self):
        """
        String representation of the user.
        """
        return self.email  # Return the user's email