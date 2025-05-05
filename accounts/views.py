from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator

from .serializers import UserRegisterSerializer, UserProfileSerializer, ForgotPasswordSerializer, \
    ResetPasswordSerializer

User = get_user_model()


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# Registration View
class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.is_active = False
        user.save()

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_link = f"http://localhost:3000/activate/{uid}/{token}/"

        send_mail(
            'Activate Your Account',
            f'Click the link to activate: {activation_link}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )


# Activate Account View
class ActivateView(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'detail': 'Account activated'}, status=200)
        return Response({'detail': 'Invalid token'}, status=400)


# Login View
class LoginView(generics.GenericAPIView):
    serializer_class = UserProfileSerializer

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()

        if user and user.check_password(password) and user.is_active:
            tokens = get_tokens_for_user(user)
            response = Response()
            response.set_cookie(
                key='access',
                value=tokens['access'],
                httponly=True,
                samesite='Lax'
            )
            response.data = {"detail": "Login Successful"}
            return response
        return Response({"detail": "Invalid Credentials"}, status=400)


# Logout View
class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        response = Response()
        response.delete_cookie('access')
        response.data = {"detail": "Logout Successful"}
        return response


# Forgot Password View
class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = User.objects.filter(email=email).first()
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = f"http://localhost:3000/reset-password/{uid}/{token}/"

            send_mail(
                'Reset Your Password',
                f'Click the link to reset your password: {reset_link}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
        return Response({"detail": "Password reset link sent if email exists"}, status=200)


# Reset Password View
class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, uidb64, token):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data['password']
        confirm_password = serializer.validated_data['confirm_password']

        if password != confirm_password:
            return Response({"detail": "Passwords do not match"}, status=400)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"detail": "Invalid Link"}, status=400)

        if user and default_token_generator.check_token(user, token):
            user.set_password(password)
            user.save()
            return Response({"detail": "Password reset successful"}, status=200)
        return Response({"detail": "Invalid token"}, status=400)


# Profile View
class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Profile updated'})





