from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from .forms import ProductForm
from .models import Customer_Profile,Product, Wishlist, Address, CartItem, Order
from userapp.models import CustomUser,SellerDetails
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.


#Customer

def index(request):
    user = request.user
    if user.is_anonymous:
        return render(request, 'index.html')
    elif user.is_seller:
        return render(request, 'seller_home.html')
    else:
        return render(request,'index.html')
    
def search_view(request):
    query = request.GET.get('query', '')
    results = []

    if query:
        # Perform a search query in your database based on the 'query' parameter
        # Replace this with your actual search logic
        products = Product.objects.filter(product_name__icontains=query)

        for product in products:
            results.append({
                'product_name': product.product_name,
                'category': product.product_category,
                'url': product.get_absolute_url(),  # Replace with the actual URL
            })

    return JsonResponse({'results': results})

# def search_products(request):
#     query = request.GET.get('q', '')
#     results = [] 

#     if query:
#         # Perform your search query here, for example, by filtering products based on the search query
#         results = Product.objects.filter(product_name__icontains=query)

#     # Prepare the search results as JSON data
#     search_results = [{'id':product.id,'product_name': product.product_name, 'product_category': product.product_category} for product in results]

#     response_data = {'results': search_results}
#     return JsonResponse(response_data)


def customer_allProducts(request, category='All'):
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

            messages.success(request, 'Profile added successfully', extra_tags='profile_tag') 
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
            messages.success(request, 'Address added successfully', extra_tags='add_address_tag')
            return redirect('customer_Profile') 

    context = {
        'user_profile': user_profile,
        'addresses': addresses, 
        'form_submitted': request.method == 'POST',
    }
    return render(request, 'customer_Profile.html', context)
    

def update_address(request):
    if request.method == 'POST':
        # Extract the data sent via AJAX
        address_id = request.POST.get('address_id')
        building_name = request.POST.get('building_name')
        address_type = request.POST.get('address_type')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')

        # Update the address
        address = get_object_or_404(Address, id=address_id)
        address.building_name = building_name
        address.address_type = address_type
        address.street = street
        address.city = city
        address.state = state
        address.zip_code = zip_code
        address.save()

        # You can return a JSON response to indicate a successful update
        return JsonResponse({'success': True})

    # If the request is not a POST request or not an AJAX request, return an error response
    return JsonResponse({'success': False, 'error': 'Invalid request'})


def delete_address(request, address_id):
    try:
        details = Address.objects.get(id=address_id)
        details.delete()
        return JsonResponse({'success': True})
    except Address.DoesNotExist:
        # Handle the case where the address does not exist
        return JsonResponse({'success': False})
    
@login_required(login_url='user_login')
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

@login_required(login_url='user_login')
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

@login_required(login_url='user_login')
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


def customer_OrderView(request):
    user = request.user
    # Fetch the user's orders and related products
    orders = Order.objects.filter(user=user).prefetch_related('products')

    context = {
        'orders': orders,
    }
    return render(request, 'customer_OrderView.html', context)















#cart
@login_required(login_url='user_login')
def add_to_Cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        
        if not created:
            # Update the cart item's quantity
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity

        cart_item.save()
    
    return redirect('http://127.0.0.1:8000/customer_ProductView/' + str(product_id) + '/')


def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product_id=product.id)

        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect('cart')

def cart(request): 
    cart_items = CartItem.objects.filter(user=request.user) 
    total_items = sum(cart_item.quantity for cart_item in cart_items)
    total_price = sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_items': total_items,
        'total_price': total_price,
            # ... other context variables ... 
    } 
    return render(request, 'customer_Cart.html',context) 
 
def remove_from_cart(request, product_id): 
    cart_item = get_object_or_404(CartItem, user=request.user, id=product_id) 
    print(f"Received product_id: {product_id}")  #Fixed the typo here 
    cart_item.delete() 
    return redirect('cart')

def decrease_item(request, item_id): 
    try: 
        cart_item = CartItem.objects.get(id=item_id) 
        if cart_item.quantity > 1: 
            cart_item.quantity -= 1 
            cart_item.save() 
    except CartItem.DoesNotExist: 
        pass  # Handle the case when the item does not exist in the cart 
    return redirect('cart')  # Redirect back to the cart page after decreasing the item quantity 
 
def increase_item(request, item_id): 
    try: 
        cart_item = CartItem.objects.get(id=item_id) 
        cart_item.quantity += 1 
        cart_item.save() 
    except CartItem.DoesNotExist: 
        pass  # Handle the case when the item does not exist in the cart 
    return redirect('cart')

def customer_Checkout(request):
    user = request.user
    # Fetch the user's addresses from the database
    user_addresses = Address.objects.filter(user=user)
    cart_items = CartItem.objects.filter(user=request.user) 
    total_items = sum(cart_item.quantity for cart_item in cart_items)
    total_price = sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items)
    # order = Order.objects.create(
    #     user=request.user,
    #     total_price=total_price,
    # )
    # for cart_item in cart_items:
    #     order.products.add(cart_item.product)
    # cart_items.delete()
    context = {
        'cart_items': cart_items,
        'total_items': total_items,
        'total_price': total_price,
        'user_addresses': user_addresses,
            # ... other context variables ... 
    } 
    return render(request,'customer_Checkout.html',context)

from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

class GeneratePDF(View):
    template_name = 'invoice_template.html'

    def get(self, request, *args, **kwargs):
        # Fetch order details from the database based on the order_id
        order_id = kwargs['order_id']
        order = Order.objects.get(id=order_id)

        # Render the template
        template = get_template(self.template_name)
        context = {'order': order}
        html = template.render(context)

        # Create a PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'filename=invoice_{order_id}.pdf'

        # Generate PDF using ReportLab
        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')

        return response














#Seller

def seller_home(request):
    return render(request,'seller_home.html')

@login_required(login_url='user_login')
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
            messages.success(request, "Product added successfully.", extra_tags='seller_product_add')
            return redirect('seller_addProducts')  # Redirect back to the add products page
    else:
        form = ProductForm()
    context = {'form': form}
    return render(request, 'seller_addProducts.html', context)

@login_required(login_url='user_login')
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
    user = request.user  # Get the current logged-in user
    try:
        seller_details = SellerDetails.objects.get(user=user)  # Retrieve the seller's details
    except SellerDetails.DoesNotExist:
        seller_details = None

    if request.method == "POST":
        # Update the CustomUser fields
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        # You can update other CustomUser fields here if needed

        # Update the SellerDetails fields
        if seller_details is None:
            # Create a new SellerDetails instance if it doesn't exist
            seller_details = SellerDetails(user=user)

        seller_details.store_name = request.POST.get("store-name")
        seller_details.phone_number = request.POST.get("phone-number")
        seller_details.pincode = request.POST.get("pincode")
        seller_details.building_name = request.POST.get("pickup-building")
        seller_details.pickup_address = request.POST.get("pickup-address")
        seller_details.city = request.POST.get("city")
        seller_details.state = request.POST.get("state")
        seller_details.account_holder_name = request.POST.get("account-holder-name")
        seller_details.account_number = request.POST.get("account-number")
        seller_details.bank_name = request.POST.get("bank-name")
        seller_details.branch = request.POST.get("branch")
        seller_details.ifsc_code = request.POST.get("ifsc-code")

        # Save both the CustomUser and SellerDetails instances
        user.save()
        seller_details.save()

        messages.success(request, "Profile updated successfully!") 
        return redirect('seller_Profile')  # Redirect back to the profile page after successful update

    context = {
        'seller_details': seller_details,  # Pass the seller details to the template
    }
    return render(request, 'seller_Profile.html', context)


from django.db.models import Sum
from django.db.models import Count

def seller_dashboard(request):
    return render(request, 'seller_dashboard.html')

# def get_sales_data(request):
#     # Assuming your Order model has a date field named 'order_date'
#     sales_data = Order.objects.filter(
#         user=request.user,
#         payment_status=Order.PaymentStatusChoices.SUCCESSFUL
#     ).values('order_date__month').annotate(total_sales=Sum('total_price'))

#     # Convert the QuerySet to a list of dictionaries
#     sales_data_list = list(sales_data)

#     return JsonResponse({'sales_data': sales_data_list})

def get_product_statistics(request):
    # Assuming your Product model has 'product_category' and 'product_subcategory' fields
    category_statistics = Product.objects.filter(
        seller=request.user
    ).values('product_category').annotate(product_count=Count('id'))

    subcategory_statistics = Product.objects.filter(
        seller=request.user
    ).values('product_subcategory').annotate(product_count=Count('id'))

    return JsonResponse({
        'category_statistics': list(category_statistics),
        'subcategory_statistics': list(subcategory_statistics),
    })

from django.db.models import Count

def sales_statistics(request):
    # Calculate product sales data
    product_sales_data = Product.objects.annotate(
        total_sales=Count('order__id')
    ).values('product_name', 'total_sales')

    # Convert the queryset into a dictionary suitable for the chart
    product_data = {
        'labels': [entry['product_name'] for entry in product_sales_data],
        'datasets': [{
            'data': [entry['total_sales'] for entry in product_sales_data],
            'backgroundColor': ['#FF6384', '#36A2EB', '#FFCE56']  # Adjust colors as needed
        }]
    }

    # Pass data to the template context
    context = {
        'product_data': product_data,
    }

    return render(request, 'seller_dashboard.html', context)


















#payment
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from decimal import Decimal



# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def homepage(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = Decimal(sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items))
    
    currency = 'INR'

    # Set the 'amount' variable to 'total_price'
    amount = int(total_price*100)
    # amount=20000

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(
        amount=amount,
        currency=currency,
        payment_capture='0'
    ))

    # Order id of the newly created order
    razorpay_order_id = razorpay_order['id']
    callback_url = '/paymenthandler/'

    order = Order.objects.create(
        user=request.user,
        total_price=total_price,
        razorpay_order_id=razorpay_order_id,
        payment_status=Order.PaymentStatusChoices.PENDING,
    )

    # Add the products to the order
    for cart_item in cart_items:
        order.products.add(cart_item.product)

    # Save the order to generate an order ID
    order.save()

    # Create a context dictionary with all the variables you want to pass to the template
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount,  # Set to 'total_price'
        'currency': currency,
        'callback_url': callback_url,
    }

    return render(request, 'homepage.html', context=context)


# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')

        # Verify the payment signature.
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        result = razorpay_client.utility.verify_payment_signature(
            params_dict)
        if result is False:
            # Signature verification failed.    
            return render(request, 'payment/paymentfail.html')
        else:
            # Signature verification succeeded.
            # Retrieve the order from the database
            order = Order.objects.get(razorpay_order_id=razorpay_order_id)
            cart_items = CartItem.objects.filter(user=request.user)

            # Check if all the books in the order are in the user's cart
                # Not all books are in the cart, add them to the library
            # Capture the payment with the amount from the order
            amount = int(order.total_price * 100)  # Convert Decimal to paise
            razorpay_client.payment.capture(payment_id, amount)

            # Update the order with payment ID and change status to "Successful"
            order.payment_id = payment_id
            order.payment_status = Order.PaymentStatusChoices.SUCCESSFUL
            order.save()
            
            # Update the order with payment ID and change status to "Successful

            # Redirect to a success page or return a success response
            return redirect('/')


