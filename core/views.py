from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages

def home(request):
    return render(request, "home.html")


def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # prevent duplicate users
        if User.objects.filter(username=email).exists():
            messages.error(request, "User already exists")
            return redirect("register")

        # create user securely
        User.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        messages.success(request, "Registration successful. Please login.")
        return redirect("login")

    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:
            auth_login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid email or password")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")
