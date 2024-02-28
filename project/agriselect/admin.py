from django.contrib import admin
from .models import Customer_Profile, Product, Address, Order, CartItem, Site_Logo, CustomerReview, ShippingAddress, Growbag, Season, SellerRevenue, DeliveryAgentProfile

# Register your models here.
admin.site.register(Product)
admin.site.register(Customer_Profile)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(CartItem)
admin.site.register(Site_Logo)
admin.site.register(CustomerReview)
admin.site.register(ShippingAddress)
admin.site.register(Growbag)
admin.site.register(Season)
admin.site.register(SellerRevenue)
admin.site.register(DeliveryAgentProfile)