from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
import logging

logger = logging.getLogger(__name__)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},
        }

class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    
    @action(detail=False, methods=['post'], url_path='register')
    def register_account(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                # Check if user already exists
                if User.objects.filter(email=serializer.validated_data['email']).exists():
                    return Response(
                        {"error": "User with this email already exists"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Create user with email as username
                user = User.objects.create_user(
                    username=serializer.validated_data['email'],
                    email=serializer.validated_data['email'],
                    first_name=serializer.validated_data['first_name'],
                    last_name=serializer.validated_data['last_name'],
                    password=serializer.validated_data['password']
                )
                
                # Create token for the new user
                token, _ = Token.objects.get_or_create(user=user)
                
                return Response({
                    "token": token.key,
                    "user_id": user.id,
                    "email": user.email
                }, status=status.HTTP_201_CREATED)
                
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            return Response(
                {"error": "Registration failed. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'], url_path='login')
    def user_login(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')

            if not email or not password:
                return Response(
                    {"error": "Both email and password are required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response(
                    {"error": "User with this email does not exist"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Authenticate using email as username
            user = authenticate(username=email, password=password)
            
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({
                    "token": token.key,
                    "user_id": user.id,
                    "email": user.email
                })
            else:
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
                
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return Response(
                {"error": "Login failed. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )