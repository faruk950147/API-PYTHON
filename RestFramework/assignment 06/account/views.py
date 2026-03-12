from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework_simplejwt.tokens import RefreshToken
from account.mixins import LogoutRequiredMixin
from account.serializers import UserSerializer

User = get_user_model()

 
@method_decorator(never_cache, name='dispatch')
class SignupView(LogoutRequiredMixin, APIView):
    def get(self, request):
        return Response({"message": "Please use POST to create an account."}, status=200)
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # built-in method handles basic validation,
            # user = serializer.save(commit=False)
            # we will handle user creation manually to add custom checks
            username = serializer.validated_data.get('username').strip()
            phone = serializer.validated_data.get('phone').strip()
            email = serializer.validated_data.get('email', None)
            password = serializer.validated_data.get('password').strip()
            
            # required check
            if not username or not phone:
                return Response({"error": "Username and phone are required."}, status=400)
            # uniqueness checks
            if User.objects.filter(username=username).exists():
                return Response({"error": "Username already exists."}, status=400)
            if User.objects.filter(phone=phone).exists():
                return Response({"error": "Phone already exists."}, status=400)
            if email and User.objects.filter(email=email).exists():
                return Response({"error": "Email already exists."}, status=400)
            if len(password) < 8:
                return Response({"error": "Password must be at least 8 characters and maximum 15 characters long."}, status=400)

            # create user
            user = User.objects.create_user(
                username=username, 
                phone=phone, email=email, 
                password=password)
            return Response({"message": "Signup successful. Please login to continue."}, status=201)

        return Response(serializer.errors, status=400)

@method_decorator(never_cache, name='dispatch')
class SignInView(APIView):
    """
    Sign In API: username / phone / email + password
    """
    def get(self, request):
        return Response({"message": "Please use POST to sign in."}, status=200)

    def post(self, request):
        identifier = request.data.get('identifier')  # phone/email/username
        password = request.data.get('password')

        if not identifier:
            return Response({"error": "Identifier required."}, status=400)
        if not password:
            return Response({"error": "Password required."}, status=400)

        # authenticate only works with username by default
        user = authenticate(request, username=identifier, password=password)

        if user is not None:
            # Session-based login → login(request, user) → Django server cookie remember user.
            # login(request, user)
            # JWT login → RefreshToken.for_user(user) → token client get, than API request send token in header. 
            # JWT token generation
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "message": "Sign In successful."
            }, status=200)

        return Response({"error": "Invalid credentials."}, status=400)

class SignOutView(APIView):
    def post(self, request):
        refresh_token = request.data.get("refresh")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()  # blacklist the token
            return Response({"message": "Sign out successfully."})
        return Response({"error": "Refresh token required."}, status=400)