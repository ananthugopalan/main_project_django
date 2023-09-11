from django.contrib.auth import get_user_model
from django.db import models


CustomUser = get_user_model()

class Products(models.Model):
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    product_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    product_category = models.CharField(max_length=100)
    product_subcategory = models.CharField(max_length=100)
    product_image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.product_name
