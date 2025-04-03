from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import login, authenticate, logout
# from users.forms import SignupForm, UserLoginForm

# # Create your views here.
# def signup_view(request):
#     if request.method == "POST":
#         form = SignupForm(request.POST)
#         print("\n\nform:", form, "\n\n")
#         print("\n\nform.is_valid():", form.is_valid(), "\n\n")
#         if form.is_valid():
#             user = form.save()
#             print(user)
#             login(request, user)
#             return redirect("applications:home")
#     else:
#         form = SignupForm()

#     return render(request, "users/signup.html", {"form": form})

# def login_view(request):
#     if request.method == 'POST':
#         form = UserLoginForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data
#             user = authenticate(
#                 request, email=data['email'], password=data['password']
#             )
#             if user is not None:
#                 login(request, user)
#                 return redirect('applications:home')
#             else:
#                 messages.error(
#                     request, 'username or password is wrong', 'danger'
#                 )
#                 return redirect('users:login')
#     else:
#         form = UserLoginForm()
#     return render(request, "users/login.html", {"form": form})

# def logout_view(request):
#     logout(request)
#     return redirect("users:login")

# @login_required
# def update_profile(request):
#     if request.method == 'POST':
#         user = request.user
        
#         # Update user fields
#         user.iin = request.POST.get('iin')
#         # user.email = request.POST.get('email')
#         user.first_name = request.POST.get('first_name')
#         user.last_name = request.POST.get('last_name')
#         user.phone_number = request.POST.get('phone_number')
        
#         # Handle profile picture upload
#         if 'profile_picture' in request.FILES:
#             user.profile_picture = request.FILES['profile_picture']
        
#         # Save the user
#         user.save()
        
#         # Add success message
#         messages.success(request, 'Profile updated successfully!')
        
#         return redirect('users:profile')
    
#     # If not POST, redirect to profile page
#     return redirect('profile')

# @login_required
# def delete_account(request):
#     if request.method == "POST":
#         user = request.user
#         user.delete()
#         logout(request)
#         messages.success(request, "Your account has been deleted.")
#         return redirect("applications:home")
#     # return render(request, "delete_account.html")

def profile_view(request):
    return render(request, "users/profile.html")

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import login, logout
from django.shortcuts import render
from .serializers import UserSerializer, SignupSerializer, LoginSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.urls import reverse

class SignupView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return render(request, "users/signup.html")

    @swagger_auto_schema(
        request_body=SignupSerializer,
        responses={
            201: UserSerializer,
            400: "Bad Request"
        },
        operation_description="Register a new user"
    )
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response({
                'message': 'User created successfully',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return render(request, "users/login.html")

    
    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            200: UserSerializer,
            400: "Bad Request"
        },
        operation_description="Login a user"
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response({
                'message': 'Login successful',
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        responses={
            200: openapi.Response('Success', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING)
                }
            ))
        },
        operation_description="Logout current user"
    )

    def post(self, request):
        logout(request)
        return Response({
            'message': 'Successfully logged out'
        }, status=status.HTTP_200_OK)

class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={
            200: UserSerializer,
            400: "Bad Request"
        },
        operation_description="Update user profile"
    )
    def post(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            if 'profile_picture' in request.FILES:
                user.profile_picture = request.FILES['profile_picture']
            serializer.save()
            return Response({
                'message': 'Profile updated successfully',
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        responses={
            200: openapi.Response('Success', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING)
                }
            ))
        },
        operation_description="Delete user account"
    )
    
    def post(self, request):
        user = request.user
        user.delete()
        logout(request)
        return Response({
            'message': 'Account successfully deleted'
        }, status=status.HTTP_200_OK)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        responses={
            200: UserSerializer
        },
        operation_description="Get user profile (returns JSON or HTML based on request)"
    )
    def get(self, request):
        if request.accepted_renderer.format == 'json':
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return render(request, "users/profile.html", {'user': request.user})