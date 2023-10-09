from django import forms
from .models import Product, Address

class ProductForm(forms.ModelForm):
    CATEGORY_CHOICES = [
        ('', '--select--'),
        ('crops', 'Crops'),
        ('seeds', 'Seeds'),
    ]

    SUBCATEGORY_CHOICES = [
        ('', '--select--'),
        ('vegetables', 'Vegetables'),
        ('fruits', 'Fruits'),
        ('flowers', 'Flowers'),
        ('cereals', 'Cereals'),
        ('herbs', 'Herbs'),
    ]
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)
    subcategory = forms.ChoiceField(choices=SUBCATEGORY_CHOICES)


    class Meta:
        model = Product
        fields = ('product_name', 'description','stock', 'category', 'subcategory','price','product_image')
        # ... other code

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['product_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Product Name'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Description', 'rows': 3})
        self.fields['price'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Price'})
        
        # Apply Bootstrap classes to the product_image field widget
        self.fields['product_image'].widget.attrs.update({'class': 'form-control', 'style': 'color: #ffffff; background-color: #007bff; border-color: #007bff;'})

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'margin-bottom: 10px;'



class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'

from .models import UploadedImage

class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['image']