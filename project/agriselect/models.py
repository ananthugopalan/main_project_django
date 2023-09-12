from django.contrib.auth import get_user_model
from django.db import models


CustomUser = get_user_model()

class Product(models.Model):
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    product_name = models.CharField(max_length=100)
    description = models.TextField()
    stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    product_category = models.CharField(max_length=100)
    product_subcategory = models.CharField(max_length=100)
    product_image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.product_name
  

class Customer_Profile(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user.email
    
class Wishlist(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField('Product')

    def __str__(self):
        return self.user.email



class SellerProfile(models.Model):
    seller = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    seller_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    business_name = models.CharField(max_length=255, blank=True, null=True)
    registration_number = models.CharField(max_length=255, blank=True, null=True)
    seller_logo = models.ImageField(upload_to='seller_logos/', blank=True, null=True)
    bank_account_details = models.CharField(max_length=255, blank=True, null=True)
    payment_method = models.CharField(max_length=20, choices=[('bank_transfer', 'Bank Transfer'), ('paypal', 'PayPal'), ('upi', 'UPI')], blank=True, null=True)
    seller_description = models.TextField(blank=True, null=True)
    shipping_locations = models.CharField(max_length=255, blank=True, null=True)
    shipping_policies = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.seller_name


class Address(models.Model):
    ADDRESS_TYPE_CHOICES = [
        ('home', 'Home'),
        ('work', 'Work'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Add a foreign key to CustomUser
    building_name = models.CharField(max_length=255)
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPE_CHOICES, default='home')
    street = models.CharField(max_length=255)  # Change "address" to "street"
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user.email} - {self.address_type}"
    

# class Cart(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

#     def __str__(self):
#         return f'Cart for {self.user.email}'

# class CartItem(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     price_per_item = models.DecimalField(max_digits=10, decimal_places=2)  # Price per item
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)      # Total price for this item

#     def __str__(self):
#         return f'{self.user.email} {self.product.product_name} ({self.quantity})'

#     def save(self, *args, **kwargs):
#         # Calculate the total price for this cart item
#         self.total_price = self.quantity * self.price_per_item
#         super().save(*args, **kwargs)

#     def update_cart_total(self):
#         cart_items = CartItem.objects.filter(cart=self.cart)
#         total = sum(cart_item.total_price for cart_item in cart_items)
#         self.cart.total_price = total
#         self.cart.save()






