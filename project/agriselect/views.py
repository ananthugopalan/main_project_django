from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from .forms import ProductForm
from .models import Customer_Profile,Product, SellerProfile,Wishlist, Address
from django.contrib import messages
from django.core.paginator import Paginator
# Create your views here.

def index(request):
    return render(request,'index.html')

def search_products(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        # Perform your search query here, for example, by filtering products based on the search query
        results = Product.objects.filter(product_name__icontains=query)

    # Prepare the search results as JSON data
    search_results = [{'id':product.id,'product_name': product.product_name, 'product_category': product.product_category} for product in results]

    response_data = {'results': search_results}
    return JsonResponse(response_data)


def customer_allProducts(request, category='All', subcategory='All'):
    if category == 'All':
        products = Product.objects.all()
    else:
        products = Product.objects.filter(product_category=category)
    categories = Product.objects.values_list('product_category', flat=True).distinct()
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'customer_allProducts.html', {'page': page,'products': products, 'selected_category': category, 'categories': categories})

def customer_Profile(request):
    user_profile, created = Customer_Profile.objects.get_or_create(customer=request.user)
    addresses = Address.objects.filter(user_id=request.user.id)
    if request.method == 'POST':
        # Check which form was submitted based on the button clicked
        if 'profile_save_button' in request.POST:
            # Handle profile form submission
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            mobile_number = request.POST.get('mobile_number')

            # Update the user profile fields
            user_profile.first_name = first_name
            user_profile.last_name = last_name
            user_profile.mobile_number = mobile_number
            user_profile.save()

            messages.success(request, 'Profile added successfully') 
            return redirect('customer_Profile')  # Display a success message

        elif 'address_save_button' in request.POST:
            # Handle address form submission
            building_name = request.POST.get('building_name')
            address_type = request.POST.get('address_type')
            street = request.POST.get('street')
            city = request.POST.get('city')
            state = request.POST.get('state')
            zip_code = request.POST.get('zip_code')            
            
            address = Address(
                user=request.user,
                building_name=building_name,
                address_type=address_type,
                street=street,
                city=city,
                state=state,
                zip_code=zip_code
            )
            address.save()
            messages.success(request, 'Address added successfully')
            return redirect('customer_Profile') 

        elif 'update_address_form' in request.POST:
            # Handle address form submission
            address_id = request.POST.get('address_id')
            address = get_object_or_404(Address, id=address_id)
            address.building_name = request.POST.get('building_name')
            address.address_type = request.POST.get('address_type')
            address.street = request.POST.get('street')
            address.city = request.POST.get('city')
            address.state = request.POST.get('state')
            address.zip_code = request.POST.get('zip_code')            
            
            address.save()
            messages.success(request, 'Address updated successfully')   # Display a success message
            return redirect('customer_Profile') 

    context = {
        'user_profile': user_profile,
        'addresses': addresses, 
        'form_submitted': request.method == 'POST',
    }
    return render(request, 'customer_Profile.html', context)

def delete_address(request, address_id):
    try:
        details = Address.objects.get(id=address_id)
        details.delete()
        return JsonResponse({'success': True})
    except Address.DoesNotExist:
        # Handle the case where the address does not exist
        return JsonResponse({'success': False})

def customer_Wishlist(request):
    if request.user.is_authenticated:
        user_wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        products = user_wishlist.products.all()
        paginator = Paginator(products, 6)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        return render(request, 'customer_Wishlist.html', {'user': request.user, 'wishlist': user_wishlist, 'page': page})
    else:
        return render(request, 'customer_Wishlist.html', {'user': None, 'wishlist': None})

def add_to_wishlist(request, product_id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=product_id)
        user_wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        user_wishlist.products.add(product)
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})
    
def remove_from_wishlist(request, product_id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=product_id)
        user_wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        user_wishlist.products.remove(product)
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


def customer_ProductView(request,product_id):
    product = get_object_or_404(Product, pk=product_id)
    product_category = product.product_category
    product_subcategory = product.product_subcategory

    # Fetch related products from the same category (excluding the current product)
    related_products = Product.objects.filter(  
        product_category=product_category
    ).exclude(pk=product_id)[:4]  # Adjust the number of related products as needed

    context = {
        'product': product,
        'product_category': product_category,
        'product_subcategory': product_subcategory,
        'related_products': related_products,
    }

    return render(request, 'customer_ProductView.html', context)

def customer_Cart(request):
    return render(request, 'customer_Cart.html')




def seller_home(request):
    return render(request,'seller_home.html')

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
            messages.success(request, "Product added successfully.")
            return redirect('seller_addProducts')  # Redirect back to the add products page
    else:
        form = ProductForm()
    context = {'form': form}
    return render(request, 'seller_addProducts.html', context)


def seller_Products(request):
    products = Product.objects.filter(seller=request.user)  # Fetch products associated with the currently logged-in seller
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page,'products': products}
    return render(request, 'seller_Products.html', context)

def delete_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        product.delete()
        # Optionally, you can add a success message here
    except Product.DoesNotExist:
        # Handle the case where the product does not exist
        pass
    return redirect('seller_Products')

def seller_updateProduct(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            # Add a success message if needed
            return redirect('seller_Products')  # Redirect back to the products list
    else:
        form = ProductForm(instance=product)

    return render(request, 'seller_updateProduct.html', {'form': form, 'product': product})

def seller_Profile(request):
    if request.method == 'POST':
        # Get the currently logged-in user
        user = request.user

        # Get data from the form
        seller_name = request.POST.get('seller_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        business_name = request.POST.get('business_name')
        registration_number = request.POST.get('registration_number')
        seller_logo = request.FILES.get('seller_logo')  # Handle file upload
        bank_account_details = request.POST.get('bank_account_details')
        payment_method = request.POST.get('payment_method')
        seller_description = request.POST.get('seller_description')
        shipping_locations = request.POST.get('shipping_locations')
        shipping_policies = request.POST.get('shipping_policies')

        # Check if seller_name is provided (it's a required field)
        if not seller_name:
            return render(request, 'seller_Profile.html', {'error_message': 'Seller Name is required'})

        # Create a SellerProfile instance and save it
        seller_profile = SellerProfile(
            seller=user,  # Assign the currently logged-in user
            seller_name=seller_name,
            email=email,
            phone_number=phone_number,
            address=address,
            business_name=business_name,
            registration_number=registration_number,
            seller_logo=seller_logo,  # Save the uploaded file
            bank_account_details=bank_account_details,
            payment_method=payment_method,
            seller_description=seller_description,
            shipping_locations=shipping_locations,
            shipping_policies=shipping_policies
        )
        seller_profile.save()
        return redirect('seller_home')
    return render(request,'seller_Profile.html')

