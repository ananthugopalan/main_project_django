from django.shortcuts import render
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from .import views

# Create your views here.

urlpatterns = [
    path('',views.customerReg,name='customer_Registration'),
    path('email-verification/<str:uidb64>/<str:token>/', views.email_verification, name='email_verification'),
    # path('verify_email/', views.verify_email, name='verify_email'),
    path('seller_registration/',views.seller_registration,name='seller_Registration'),
    path('user_login/',views.user_login,name='user_login'),
    path('user_logout/',views.user_logout,name='user_logout'),
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('accounts/',include('allauth.urls')),  
    
]
