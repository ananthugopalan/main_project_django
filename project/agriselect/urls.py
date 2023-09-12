from django.contrib import admin
from django.urls import path,include
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('search/', views.search_products, name='search_products'),
    path('customer_allProducts/',views.customer_allProducts,name='customer_allProducts'),
    path('customer_ProductView/<int:product_id>/',views.customer_ProductView,name='customer_ProductView'),
    path('customer_Profile/', views.customer_Profile, name='customer_Profile'),
    path('customer_Wishlist/',views.customer_Wishlist,name='customer_Wishlist'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('customer_allProducts/<str:category>/', views.customer_allProducts, name='customer_allProducts'),
    path('customer_Cart/', views.customer_Cart, name='customer_Cart'),
    path('seller_home/',views.seller_home,name='seller_home'),
    path('seller_Profile/',views.seller_Profile,name='seller_Profile'),
    path('seller_addProducts/', views.seller_addProducts, name='seller_addProducts'),
    path('seller_updateProduct/<int:product_id>/', views.seller_updateProduct, name='seller_updateProduct'),
    path('seller_Products/',views.seller_Products,name='seller_Products'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('delete_address/<int:address_id>/', views.delete_address, name='delete_address'),
]
