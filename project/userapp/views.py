from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth import authenticate, login as auth_login

# Create your views here.

def customerReg(request):
    if request.method=='POST':
        name = request.POST.get('name') 
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')
        # role = CustomUser.CUSTOMER
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "User with this email already exists.")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match.")
        elif name and email and password:
            user = CustomUser(name=name, email=email, role=CustomUser.CUSTOMER) 
            user.set_password(password)
            user.save()
            messages.success(request, "Registration successful! Sign in to your account.")
            return redirect('user_login')
    return render(request, 'customerReg.html')


def sellerReg(request):
    if request.method=='POST':
        name = request.POST.get('name') 
        email = request.POST.get('email')
        password = request.POST.get('password')   
        confirm_password = request.POST.get('confirmPassword')     
        # role = CustomUser.SELLER
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "User with this email already exists.")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match.")
        elif name and email and password:
            user = CustomUser(name=name, email=email, role=CustomUser.SELLER)
            user.set_password(password)            
            user.save()
            messages.success(request, "Registration successful! Sign in to your account.")
            return redirect('user_login')
    return render(request, 'sellerReg.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email and password:
            user = authenticate(request, email=email, password=password)
            if user is not None:
                auth_login(request, user) 
                if user.role == CustomUser.SELLER:       
                    return redirect('seller_home')
                else:
                    return redirect('/')
            else:
                error_message = "Invalid login credentials."
                return render(request, 'login.html', {'error_message': error_message})
    return render(request,'login.html')


def user_logout(request):
    auth.logout(request)
    return redirect('/') 
