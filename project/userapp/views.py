from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .models import CustomUser, SellerDetails
from django.contrib.auth import authenticate, login as auth_login 


# Create your views here.

def email_verification(request, uidb64, token):
    User = get_user_model()
    try:
        user_id = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=user_id)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Email verification successful! You can now log in.")
        else:
            messages.error(request, "Email verification failed. Please request a new verification email.")
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    return redirect('user_login')

def customerReg(request):
    if request.method=='POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name') 
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')
        # role = CustomUser.CUSTOMER
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "User with this email already exists.")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match.")
        elif first_name and last_name and email and password:
            user = CustomUser(first_name=first_name,last_name=last_name, email=email) 
            user.set_password(password)
            user.is_customer = True
            user.is_active = False
            user.save()

            # Generate a verification token
            token = default_token_generator.make_token(user)

            # Create the verification URL with the token
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            verification_url = reverse('email_verification', args=[uidb64, token])

            # Construct the email message with the verification URL
            message = f"Click the following link to verify your email: {request.build_absolute_uri(verification_url)}"

            # Send the verification email
            send_mail(
                'Email Verification',
                message,
                'agriselect1@gmail.com',  # Replace with your sender email
                [user.email],
                fail_silently=False,
            )

            messages.success(request, "Registration successful! Please check your email to verify your account.")
        else:
            messages.error(request, "Registration failed. Please try again.")
    return render(request, 'customerReg.html')

def seller_registration(request):
    if request.method == 'POST': 
        step = request.POST.get('step') 
 
        print(step) 
        # Check which step the form data is coming from 
        if step == '1': 
            print("one") 
            # Step 1 Data 
            first_name = request.POST.get('first_name') 
            last_name = request.POST.get('last_name') 
            email = request.POST.get('email') 
            password = request.POST.get('password')  
            pan_number = request.POST.get('pan_number') 
        
            # Check for existing user with the same email 
            if CustomUser.objects.filter(email=email).exists(): 
                messages.error(request, "Email already exists.", extra_tags='seller_reg') 
            else: 
                # Create a new user and set the password 
                user = CustomUser(first_name=first_name,last_name=last_name, pan_number=pan_number, email=email)  
                user.set_password(password)  # Hash the password
                user.is_active = False 
                user.is_seller = True
                user.save() 
 
                # Store the user ID in the session for future steps 
                request.session['user_id'] = user.id 
 
                messages.success(request, "Step 1 completed successfully.", extra_tags='seller_reg') 
                # Redirect to step 2 or confirmation page 
 
        elif step == '2': 
            print("two") 
            # Step 2 Data 
            user_id = request.session.get('user_id') 
            if user_id: 
                user = CustomUser.objects.get(id=user_id) 
                
                store_name = request.POST.get('store-name') 
                phone_number = request.POST.get('phone-number') 
                pincode = request.POST.get('pincode') 
                building_name = request.POST.get('pickup-building') 
                pickup_address = request.POST.get('pickup-address') 
                city = request.POST.get('city') 
                state = request.POST.get('state') 
 
                # Check if the user already has seller details 
                seller_details, created = SellerDetails.objects.get_or_create(user=user) 
 
                # Update the seller details 
                
                seller_details.store_name = store_name 
                seller_details.phone_number = phone_number 
                seller_details.pincode = pincode 
                seller_details.building_name = building_name
                seller_details.pickup_address = pickup_address 
                seller_details.city = city 
                seller_details.state = state 
                seller_details.save() 
 
                messages.success(request, "Step 2 completed successfully.", extra_tags='seller_reg') 
                # Redirect to step 3 or confirmation page 
 
        elif step == '3': 
            print("three") 
            # Step 3 Data 
            user_id = request.session.get('user_id') 
            if user_id: 
                user = CustomUser.objects.get(id=user_id) 
                 
                account_holder_name = request.POST.get('account-holder-name') 
                account_number = request.POST.get('account-number') 
                bank_name = request.POST.get('bank-name') 
                branch = request.POST.get('branch') 
                ifsc_code = request.POST.get('ifsc-code') 
 
                # Check if the user already has seller details 
                seller_details, created = SellerDetails.objects.get_or_create(user=user) 
 
                # Update the seller details 
                seller_details.account_holder_name = account_holder_name 
                seller_details.account_number = account_number 
                seller_details.bank_name = bank_name 
                seller_details.branch = branch 
                seller_details.ifsc_code = ifsc_code 
                seller_details.save() 

                user.is_active = True  # Activate the user 
                user.save() 
 
                # Generate a verification token
                token = default_token_generator.make_token(user)
 
                # Create the verification URL with the token
                uidb64 = urlsafe_base64_encode(user.pk.to_bytes(4, byteorder='big'))
                verification_url = reverse('email_verification', args=[uidb64, token])
 
                # Construct the email message with the verification URL
                message = f"Click the following link to verify your email: {request.build_absolute_uri(verification_url)}"
 
                # Send the verification email
                send_mail(
                    'Email Verification',
                    message,
                    'agriselect1@gmail.com',  # Replace with your sender email
                    [user.email],
                    fail_silently=False,
                )
 
                messages.success(request, "Registration completed successfully. Please check your email to verify your account.", extra_tags='seller_reg')
                # Clear the user ID from the session as registration is complete
                del request.session['user_id']              

    return render(request, 'seller_registration.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email and password:
            user = authenticate(request, email=email, password=password)
            if user is not None:
                auth_login(request, user) 
                if user.is_seller:      
                    return redirect('seller_home')
                elif user.is_customer: 
                    return redirect('/')
            else:
                error_message = "Invalid login credentials."
                return render(request, 'login.html', {'error_message': error_message})
            
    return render(request,'login.html')


def user_logout(request):
    auth.logout(request)
    return redirect('/') 
