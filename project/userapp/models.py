from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    CUSTOMER = 1
    SELLER = 2

    ROLE_CHOICE = (
        (SELLER, 'Seller'),
        (CUSTOMER, 'Customer'),
    )
    username = None
    USERNAME_FIELD  = 'email'
    # username = models.CharField(max_length=100,unique=True, default='')
    name = models.CharField(max_length=100, default='')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True,default=CUSTOMER)
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.name
    