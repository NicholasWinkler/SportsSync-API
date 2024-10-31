from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers  # Import serializers
import logging

# Set up logging
logger = logging.getLogger(__name__)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': False}  # Make username optional
        }


class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'], url_path='register')
    def register_account(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.validated_data['email'],  # Using email as username
                email=serializer.validated_data['email'],
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name'],
                password=serializer.validated_data['password']
            )
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_201_CREATED)

        # Log the errors to the console
        logger.error('Registration error: %s', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='login')
    def user_login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        logger.debug('Login attempt for email: %s', email)

        # Fetch the user by email and then authenticate by password
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            logger.error('Login failed: user with email %s does not exist.', email)
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate using username and password
        user = authenticate(username=user.username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            logger.info('User %s logged in successfully.', email)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            logger.error('Login failed: invalid credentials for email %s.', email)
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
