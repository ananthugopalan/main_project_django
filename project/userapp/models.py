from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # CUSTOMER = 1
    # SELLER = 2

    # ROLE_CHOICE = (
    #     (SELLER, 'Seller'),
    #     (CUSTOMER, 'Customer'),
    # )
    username = None
    USERNAME_FIELD  = 'email'
    # username = models.CharField(max_length=100,unique=True, default='')
    first_name = models.CharField(max_length=100, default='')
    last_name   = models.CharField(max_length=100, default='')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    # role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True,default=CUSTOMER)
    is_customer = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    pan_number = models.CharField(max_length=25, null=True)
    
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        # If the user is being created and is not explicitly set as a seller,
        # set the default role to customer.
        if not self.pk and not self.is_seller:
            self.is_customer = True
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.first_name
    

class SellerDetails(models.Model):
    # Step 2 Fields    
    building_name = models.CharField(max_length=255,null=True)  
    store_name = models.CharField(max_length=255,null=True) 
    phone_number = models.CharField(max_length=15,null=True) 
    pincode = models.CharField(max_length=10,null=True) 
    pickup_address = models.CharField(max_length=255,null=True) 
    city = models.CharField(max_length=100,null=True) 
    state = models.CharField(max_length=100,null=True) 
    
    # Step 3 Fields 
    account_holder_name = models.CharField(max_length=255,null=True) 
    account_number = models.CharField(max_length=20,null=True) 
    bank_name = models.CharField(max_length=255,null=True) 
    branch = models.CharField(max_length=255) 
    ifsc_code = models.CharField(max_length=20) 
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='seller_details_user',null=True) 
 
    def __str__(self): 
        return self.store_name 
    class Meta: 
        verbose_name_plural = "SellerDetails"