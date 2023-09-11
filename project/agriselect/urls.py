from django.contrib import admin
from django.urls import path,include
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('seller_home/',views.seller_home,name='seller_home'),
    path('customer_Profile/',views.customer_Profile,name='customer_Profile'),
    path('seller_addProducts/',views.seller_addProducts,name='seller_addProducts'),
    path('seller_Products/',views.seller_Products,name='seller_Products'),
]
