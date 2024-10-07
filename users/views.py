from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer

# Get the User model
User = get_user_model()

class UserListCreateView(ListCreateAPIView):
    """
    View to list all users or create a new user.
    Accessible only to authenticated users.
    """
    queryset = User.objects.all()  # Queryset to retrieve all users
    serializer_class = UserSerializer  # Serializer for user data
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this view

class UserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a user by ID.
    Accessible only to authenticated users.
    """
    queryset = User.objects.all()  # Queryset to retrieve all users
    serializer_class = UserSerializer  # Serializer for user data
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this view