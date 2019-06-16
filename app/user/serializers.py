from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 6}
        }

    def create(self, valid_data):
        """Create a new user with encrypt password and return user"""
        return get_user_model().objects.create_user(**valid_data)
