from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Home Page - Requires login
@login_required(login_url='login')
def HomePage(request):
    return render(request, 'home.html')

# Signup Page - Handle signup and password mismatch
def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        # Check if passwords match
        if pass1 != pass2:
            messages.error(request, "Your password and confirm password are not the same!")
            return redirect('signup')
        else:
            # Create the user if passwords match
            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            messages.success(request, "Your account has been created successfully! Please log in.")
            return redirect('login')

    return render(request, 'signup.html')

# Login Page - Handle login and invalid credentials
def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('login')

    return render(request, 'login.html')

# Logout Page - Handle logout
def LogoutPage(request):
    logout(request)
    return redirect('login')
