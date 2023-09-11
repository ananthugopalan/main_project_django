from django.shortcuts import render,redirect
from .forms import ProductForm
from .models import Products
from django.contrib import messages
# Create your views here.

def index(request):
    return render(request,'index.html')

def seller_home(request):
    return render(request,'seller_home.html')

def customer_Profile(request):
    return render(request,'customer_Profile.html')

def seller_addProducts(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)  # Create a new Product instance but don't save it yet
            product.seller = request.user 
            # Manually assign the selected category and subcategory values to the model fields
            product.product_category = form.cleaned_data['category']
            product.product_subcategory = form.cleaned_data['subcategory']
            
            product.save()  # Save the complete Product instance
            messages.success(request, "Your Product added successfully.")
            return redirect('seller_addProducts')  # Redirect back to the add products page
    else:
        form = ProductForm()
    context = {'form': form}
    return render(request, 'seller_addProducts.html', context)

def seller_Products(request):
    products = Products.objects.filter(seller=request.user)  # Fetch products associated with the currently logged-in seller
    context = {'products': products}
    return render(request, 'seller_Products.html', context)
