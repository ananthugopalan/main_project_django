from django.contrib.auth import get_user_model
from django.db import models
from decimal import Decimal
from django.utils import timezone


CustomUser = get_user_model()

class Product(models.Model):
    class StatusChoices(models.TextChoices):
        IN_STOCK = 'in_stock', 'In Stock'
        DEACTIVATED = 'deactivated', 'Deactivated'
        OUT_OF_STOCK = 'out_of_stock', 'Out of Stock'

    class SeasonChoices(models.TextChoices):
        SPRING = 'spring', 'Spring'
        SUMMER = 'summer', 'Summer'
        AUTUMN = 'autumn', 'Autumn'
        WINTER = 'winter', 'Winter'
        MONSOON = 'monsoon', 'Monsoon' 

    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    product_name = models.CharField(max_length=100)
    description = models.TextField()
    stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    product_category = models.CharField(max_length=100)
    product_subcategory = models.CharField(max_length=100)
    product_image = models.ImageField(upload_to='product_images/')
    average_rating = models.FloatField(default=0.0)
    status = models.CharField(
        max_length=20, choices=StatusChoices.choices, default=StatusChoices.IN_STOCK
    )
    season = models.ManyToManyField(
        'Season', related_name='products', blank=True
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.product_name

class Season(models.Model):
    name = models.CharField(max_length=20, choices=Product.SeasonChoices.choices, unique=True)

    def __str__(self):
        return self.name
  

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
    DISTRICT_CHOICES = [
        ('Alappuzha', 'Alappuzha'),
        ('Ernakulam', 'Ernakulam'),
        ('Idukki', 'Idukki'),
        ('Kannur', 'Kannur'),
        ('Kasaragod', 'Kasaragod'),
        ('Kollam', 'Kollam'),
        ('Kottayam', 'Kottayam'),
        ('Kozhikode', 'Kozhikode'),
        ('Malappuram', 'Malappuram'),
        ('Palakkad', 'Palakkad'),
        ('Pathanamthitta', 'Pathanamthitta'),
        ('Thiruvananthapuram', 'Thiruvananthapuram'),
        ('Thrissur', 'Thrissur'),
        ('Wayanad', 'Wayanad'),
    ]
    LOCATION_CHOICES = (
        ('Ernakulam', 'Ernakulam'),
        ('Malappuram', 'Malappuram'),
        ('Kannur', 'Kannur'),
        # Add more locations as needed
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Add a foreign key to CustomUser
    building_name = models.CharField(max_length=255)
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPE_CHOICES, default='home')
    street = models.CharField(max_length=255)  # Change "address" to "street"
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100, choices=DISTRICT_CHOICES, blank=True, null=True)
    location = models.CharField(max_length=100, choices=LOCATION_CHOICES, blank=True, null=True)
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
    dispatched = models.BooleanField(default=False)  
    accepted_by_store = models.BooleanField(default=False)
    ready_for_pickup = models.BooleanField(default=False)  # New field

    def __str__(self):
        return f'{self.quantity} x {self.product.product_name} ({self.status})'
    
    def save(self, *args, **kwargs):
        # Calculate and set the total price and total items
        self.total_price = self.product.price * self.quantity
        self.total_items = self.quantity
        
        super().save(*args, **kwargs)

from django.utils import timezone
class Order(models.Model):
    class PaymentStatusChoices(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SUCCESSFUL = 'successful', 'Successful'
        FAILED = 'failed', 'Failed'
    
    class OrderStatusChoices(models.TextChoices):
        REQUESTED = 'Requested', 'Requested'
        DISPATCHED = 'Dispatched', 'Dispatched'
        DELIVERED = 'Delivered', 'Delivered'

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cart_items = models.ManyToManyField('CartItem')  # Assuming the CartItem model has a reference to Product
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date_only = models.DateField(default=timezone.now)
    order_date = models.DateTimeField(auto_now_add=True)
    razorpay_order_id = models.CharField(max_length=255, default=None)
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    payment_status = models.CharField(
        max_length=20, choices=PaymentStatusChoices.choices, default=PaymentStatusChoices.PENDING)
    order_status = models.CharField(
        max_length=20, choices=OrderStatusChoices.choices, default=OrderStatusChoices.REQUESTED)
    accepted_by_store = models.BooleanField(default=False)
    ready_for_pickup = models.BooleanField(default=False)  # New field

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

from django.db.models import Avg
class CustomerReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    sentiment_score = models.FloatField(null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update the average rating of the associated product
        self.product.average_rating = CustomerReview.objects.filter(product=self.product).aggregate(Avg('rating'))['rating__avg'] or 0
        self.product.save()
    
    def __str__(self):
        return f'{self.user.email} - {self.product.product_name}'
    

class Growbag(models.Model):
    COLOR_CHOICES = [
        ('brown', 'Brown'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('violet', 'Violet'),
        ('red', 'Red'),
        ('purple', 'Purple'),
        # Add other color options as needed
    ]
    
    SIZE_CHOICES = [
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('regular', 'Regular'),
        # Add other size options as needed
    ]
    
    ICON_CHOICES = [
        ('sun', 'Sun'),
        ('leaf', 'Leaf'),
        ('water', 'Water'),
        ('globe', 'Globe'),
        ('heart', 'Heart'),
        ('tree', 'Tree'),
        ('moon', 'Moon'),
        ('plant', 'Plant'),
        ('vegetable', 'Vegetable'),
        ('fruit', 'Fruit'),
        ('crops', 'Crops'),
        ('cannabis', 'Cannabis'),
    ]

    color_chosen = models.CharField(max_length=255, choices=COLOR_CHOICES, default='brown')
    size_chosen = models.CharField(max_length=255, choices=SIZE_CHOICES, default='regular')
    drainage_holes = models.BooleanField(default=False, null=True, blank=True)
    icon_chosen = models.CharField(max_length=255, choices=ICON_CHOICES, null=True, blank=True)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    qty = models.PositiveIntegerField(default=1)  # Field for quantity
    image = models.ImageField(upload_to='growbag_images/', null=True, blank=True)

    def __str__(self):
        return f"Growbag - {self.color_chosen} - {self.size_chosen}"

class Notification(models.Model):
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderNotification(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class SellerRevenue(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    revenue = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order ID: {self.order.id}, Seller: {self.seller.email}, Revenue: {self.revenue}"
    

class AdminSettings(models.Model):
    # Define choices for seasons
    SEASON_CHOICES = [
        ('spring', 'Spring'),
        ('summer', 'Summer'),
        ('autumn', 'Autumn'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
    ]

    # Add fields for various settings, including the selected season
    selected_season = models.CharField(max_length=20, choices=SEASON_CHOICES,default='summer')


class DeliveryAgentProfile(models.Model):
    delivery_agent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True, default=None) 
    address = models.TextField()
    phone = models.CharField(max_length=15)
    LOCATION_CHOICES = (
        ('Ernakulam', 'Ernakulam'),
        ('Malappuram', 'Malappuram'),
        ('Kannur', 'Kannur'),
        # Add more locations as needed
    )
    location = models.CharField(max_length=100, choices=LOCATION_CHOICES)
    aadhaar_number = models.CharField(max_length=12, unique=True)
    driver_license_number = models.CharField(max_length=50, unique=True)
    employee_id = models.CharField(max_length=10, unique=True, default=None)
    vehicle_type = models.CharField(max_length=100, blank=True, null=True)
    vehicle_number = models.CharField(max_length=20, unique=True)
    BANK_CHOICES = (
        ('ALLAHABAD BANK', 'Allahabad Bank'),
        ('ANDHRA BANK', 'Andhra Bank'),
        ('AXIS BANK', 'Axis Bank'),
        ('BANK OF BARODA', 'Bank of Baroda'),
        ('BANK OF INDIA', 'Bank of India'),
        ('BANK OF MAHARASHTRA', 'Bank of Maharashtra'),
        ('CANARA BANK', 'Canara Bank'),
        ('CORPORATION BANK', 'Corporation Bank'),
        ('HONG KONG & SHANGHAI BANK', 'Hong Kong & Shanghai Bank'),
        ('INDIAN BANK', 'Indian Bank'),
        ('INDIAN OVERSEAS BANK', 'Indian Overseas Bank'),
        ('KARUR VYSYA BANK', 'Karur Vysya Bank'),
        ('NORTH MALABAR GRAMIN BANK', 'North Malabar Gramin Bank'),
        ('ORIENTAL BANK OF COMMERCE', 'Oriental Bank of Commerce'),
        ('PUNJAB AND SIND BANK', 'Punjab and Sind Bank'),
        ('PUNJAB NATIONAL BANK', 'Punjab National Bank'),
        ('RESERVE BANK OF INDIA', 'Reserve Bank of India'),
        ('SOUTH INDIAN BANK', 'South Indian Bank'),
        ('STANDARD CHARTERED BANK', 'Standard Chartered Bank'),
        ('STATE BANK OF BIKANER AND JAIPUR', 'State Bank of Bikaner and Jaipur'),
        ('STATE BANK OF HYDERABAD', 'State Bank of Hyderabad'),
        ('STATE BANK OF MYSORE', 'State Bank of Mysore'),
        ('STATE BANK OF PATIALA', 'State Bank of Patiala'),
        ('STATE BANK OF TRAVANCORE', 'State Bank of Travancore'),
        ('SYNDICATE BANK', 'Syndicate Bank'),
        ('LAKSHMI VILAS BANK LTD', 'Lakshmi Vilas Bank Ltd'),
        ('UCO BANK', 'UCO Bank'),
        ('UNION BANK OF INDIA', 'Union Bank of India'),
        ('UNITED BANK OF INDIA', 'United Bank of India'),
        ('VIJAYA BANK', 'Vijaya Bank'),
        ('CENTRAL BANK OF INDIA', 'Central Bank of India'),
        ('DENA BANK', 'Dena Bank'),
        ('BANDHAN BANK LIMITED', 'Bandhan Bank Limited'),
        ('KERALA GRAMIN BANK', 'Kerala Gramin Bank'),
        ('LAXMI VILAS BANK', 'Laxmi Vilas Bank'),
        ('BANK OF BAHARAIN AND KUWAIT BSC', 'Bank of Baharain and Kuwait BSC'),
        ('BHARATIYA MAHILA BANK LIMITED', 'Bharatiya Mahila Bank Limited'),
        ('CATHOLIC SYRIAN BANK', 'Catholic Syrian Bank'),
        ('CITIBANK NA', 'Citibank NA'),
        ('CITY UNION BANK LTD', 'City Union Bank Ltd'),
        ('DEVELOPMENT CREDIT BANK', 'Development Credit Bank'),
        ('DHANALAXMI BANK', 'Dhanalaxmi Bank'),
        ('DOHA BANK', 'Doha Bank'),
        ('FEDERAL BANK LTD', 'Federal Bank Ltd'),
        ('HDFC BANK LTD', 'HDFC Bank Ltd'),
        ('ICICI BANK LTD', 'ICICI Bank Ltd'),
        ('IDBI BANK LTD', 'IDBI Bank Ltd'),
        ('ING VYSYA BANK LTD', 'ING Vysya Bank Ltd'),
        ('INDUSIND BANK LTD', 'IndusInd Bank Ltd'),
        ('JAMMU AND KASHMIR BANK LTD', 'Jammu and Kashmir Bank Ltd'),
        ('KARNATAKA BANK LTD', 'Karnataka Bank Ltd'),
        ('KOTAK MAHINDRA BANK', 'Kotak Mahindra Bank'),
        ('STATE BANK OF INDIA', 'State Bank of India'),
        ('TAMILNAD MERCANTILE BANK LTD', 'Tamilnad Mercantile Bank Ltd'),
        ('YES BANK LTD', 'Yes Bank Ltd'),
        ('OTHER', 'Other'),
    )
    bank_name = models.CharField(max_length=100, choices=BANK_CHOICES)
    branch = models.CharField(max_length=100)
    account_number = models.CharField(max_length=18)
    ifsc_code = models.CharField(max_length=11)
    id_document = models.FileField(upload_to='id_documents/', blank=True, null=True)


    def save(self, *args, **kwargs):
            # Generate a unique employee ID if it's not already set
            if not self.employee_id:
                last_id = DeliveryAgentProfile.objects.order_by('-id').first()
                last_id = int(last_id.employee_id.split('AS')[1]) if last_id else 0
                new_id = last_id + 1
                self.employee_id = f'AS{new_id:04}'
            super().save(*args, **kwargs)
    