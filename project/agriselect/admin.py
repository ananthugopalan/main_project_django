from django.contrib import admin
from .models import Customer_Profile, Product, Address

# Register your models here.
admin.site.register(Product)
admin.site.register(Customer_Profile)
admin.site.register(Address)
