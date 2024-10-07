from django.contrib.auth import get_user_model
from rest_framework import serializers

# Get the User model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model to handle user data serialization and deserialization.
    """
    class Meta:
        model = User  # Specify the model to serialize
        fields = ['id', 'email', 'username', 'password']  # Fields to be included in the serialized output
        extra_kwargs = {
            'password': {'write_only': True}  # Password should be write-only for security
        }
        
    def create(self, validated_data):
        """
        Create a new user instance with the validated data.
        """
        user = User.objects.create_user(**validated_data)  # Create user with hashed password
        return user
    
    def update(self, instance, validated_data):
        """
        Update an existing user instance with the validated data.
        """
        # Update email and username if provided
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)

        # Update password if provided
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])  # Hash the new password
        instance.save()  # Save the updated instance
        return instance