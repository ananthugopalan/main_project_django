from django.contrib.auth import get_user_model
from django.db import models


CustomUser = get_user_model()

class Product(models.Model):
    class StatusChoices(models.TextChoices):
        IN_STOCK = 'in_stock', 'In Stock'
        DEACTIVATED = 'deactivated', 'Deactivated'
        OUT_OF_STOCK = 'out_of_stock', 'Out of Stock'
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    product_name = models.CharField(max_length=100)
    description = models.TextField()
    stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    product_category = models.CharField(max_length=100)
    product_subcategory = models.CharField(max_length=100)
    product_image = models.ImageField(upload_to='product_images/')
    status = models.CharField(
        max_length=20, choices=StatusChoices.choices, default=StatusChoices.IN_STOCK
    )

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
    class StatusChoices(models.TextChoices):
        ACTIVE = 'active', 'Active'
        CLEARED = 'cleared', 'Cleared'
        ORDERED = 'ordered', 'Ordered'
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True)
    status = models.CharField(
        max_length=10,null=True, choices=StatusChoices.choices, default=StatusChoices.ACTIVE
    )

    def __str__(self):
        return f'{self.quantity} x {self.product.product_name} ({self.status})'
    
    def save(self, *args, **kwargs):
        # Calculate and set the total price and total items
        self.total_price = self.product.price * self.quantity
        self.total_items = self.quantity
        
        super().save(*args, **kwargs)

class Order(models.Model):
    class PaymentStatusChoices(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SUCCESSFUL = 'successful', 'Successful'
        FAILED = 'failed', 'Failed'

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cart_items = models.ManyToManyField('CartItem')  # Assuming the CartItem model has a reference to Product
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    razorpay_order_id = models.CharField(max_length=255, default=None)
    payment_status = models.CharField(
        max_length=20, choices=PaymentStatusChoices.choices, default=PaymentStatusChoices.PENDING)
    def __str__(self):
        return self.user.email


class Site_Logo(models.Model):
    logo_img = models.ImageField(upload_to='images')

class ShippingAddress(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SHIPPED = 'shipped', 'Shipped'
        DELIVERED = 'delivered', 'Delivered'
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order = models.OneToOneField('Order', on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING
    )

    def __str__(self):
        return f"{self.user.first_name} - Order ID: {self.order.id} - Status: {self.status}"


class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploads/')
    predicted_disease = models.CharField(max_length=255, blank=True, null=True)