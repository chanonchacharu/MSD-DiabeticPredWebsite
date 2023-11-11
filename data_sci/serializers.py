from rest_framework import serializers

class AuthenticationAPISerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=255)
    password = serializers.CharField(required=True)