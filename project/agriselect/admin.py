from django.contrib import admin
from .models import Customer_Profile, Product, Address, Order, CartItem

# Register your models here.
admin.site.register(Product)
admin.site.register(Customer_Profile)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(CartItem)
