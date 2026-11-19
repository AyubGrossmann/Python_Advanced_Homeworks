from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .serializers import RegisterSerializer

User = get_user_model()
ACCESS_COOKIE = "access_token"
REFRESH_COOKIE = "refresh_token"

def set_auth_cookies(response, access_token, refresh_token):
    response.set_cookie(
        ACCESS_COOKIE, access_token,
        httponly=True, secure=settings.AUTH_COOKIE_SECURE,
                samesite=settings.AUTH_COOKIE_SAMESITE,
        max_age=30 * 60, path="/",
    )
    response.set_cookie(
        REFRESH_COOKIE, refresh_token,
        httponly=True, secure=settings.AUTH_COOKIE_SECURE,
                samesite=settings.AUTH_COOKIE_SAMESITE,
        max_age=24 * 60 * 60, path="/",
    )

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "Регистрация прошла успешно.", "username": user.username},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        login_value = request.data.get("username_or_email", "").strip()
        password = request.data.get("password", "")
        if not login_value or not password:
            return Response(
                {"error": "Введите логин/email и пароль."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_by_email = User.objects.filter(email__iexact=login_value).first()
        username = user_by_email.username if user_by_email else login_value
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response(
                {"error": "Неверный логин или пароль."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)
        response = Response({"message": "Вход выполнен успешно."})
        set_auth_cookies(response, str(refresh.access_token), str(refresh))
        return response

class RefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_value = request.COOKIES.get(REFRESH_COOKIE)
        if not refresh_value:
            return Response(
                {"error": "Refresh token не найден."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            old_refresh = RefreshToken(refresh_value)
            user = User.objects.get(pk=old_refresh["user_id"])
            new_refresh = RefreshToken.for_user(user)
            old_refresh.blacklist()
            response = Response({"message": "Токены обновлены."})
            set_auth_cookies(
                response, str(new_refresh.access_token), str(new_refresh)
            )
            return response
        except (TokenError, User.DoesNotExist, KeyError):
            return Response(
                {"error": "Refresh token недействителен."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_value = request.COOKIES.get(REFRESH_COOKIE)
        if refresh_value:
            try:
                RefreshToken(refresh_value).blacklist()
            except TokenError:
                pass

        response = Response({"message": "Вы вышли из аккаунта."})
        response.delete_cookie(ACCESS_COOKIE, path="/")
        response.delete_cookie(REFRESH_COOKIE, path="/")
        return response
