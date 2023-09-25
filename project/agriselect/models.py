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
        return self.first_name
    
class Wishlist(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField('Product')

    def __str__(self):
        return self.user.email



class Address(models.Model):
    ADDRESS_TYPE_CHOICES = [
        ('Home', 'Home'),
        ('Work', 'Work'),
        ('Other', 'Other'),
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
    

class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True)
    total_items = models.PositiveIntegerField(default=0, null=True)

    def __str__(self):
        return f'{self.quantity} x {self.product.product_name}'
    
    def save(self, *args, **kwargs):
        # Calculate and set the total price and total items
        self.total_price = self.product.price * self.quantity
        self.total_items = self.quantity
        
        super().save(*args, **kwargs)



