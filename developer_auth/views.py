import json
from pyexpat.errors import messages
import secrets
from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password

from developer_auth.utils import encrypt_key, decrypt_key
from .models import Developer, APIKey, DeveloperAPIKey
from products.models import Product
from .forms import DeveloperRegisterForm, DeveloperLoginForm, DeveloperUpdateForm, DeveloperPasswordChangeForm
from django.utils import timezone
from django.http import HttpResponse
# Create your views here.
User = get_user_model()

def index(request):
    return render(request, 'developer_auth/index.html')

def docs(request):
    return render(request, 'developer_auth/docs.html')

def authentication(request):
    return render(request, 'developer_auth/authentication.html')

def prerequisite(request):
    return render(request, 'developer_auth/prerequisite.html')

def live_implementation(request):
    return render(request, 'developer_auth/live_implementation.html')

def support(request):
    return render(request, 'developer_auth/support.html')

@login_required(login_url='account_login')
def dashboard(request):
    developer = request.user
    api_key = APIKey.objects.filter(developer=developer, is_active=True).first()
    api_key.secret_key = decrypt_key(api_key.encrypted_secret_key) if api_key else None

    return render(request, 'developer_auth/dashboard.html', {'api_key': api_key})

def order(request):
    return render(request, 'developer_auth/orders.html')

from django.db.models import Q

def products(request):
    query = request.GET.get('search', '')
    products = Product.objects.filter(developer=request.user)
    
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(slug__icontains=query)
        )
    
    if request.headers.get('HX-Request'):
        return render(request, 'developer_auth/partials/product_list.html', {'products': products})
        
    return render(request, 'developer_auth/products.html', {'products': products})

@login_required(login_url='account_login')
def api_keys(request):
    keys = APIKey.objects.filter(developer=request.user).order_by('-is_active', '-created_at')
    for key in keys:
        key.secret_key = decrypt_key(key.encrypted_secret_key)

    return render(request, 'developer_auth/api_keys.html', {'keys': keys})

def webhooks(request):
    return render(request, 'developer_auth/webhooks.html')

def documetation(request):
    return render(request, 'developer_auth/documentation.html')

def revoke_key(request, public_key):
    user = request.user
    key = APIKey.objects.get(developer=user, public_key=public_key)
    key.is_active = False
    key.revoked_at = timezone.now()
    key.save()
    return redirect('api-keys')

def cheat_sheet(request):
    return render(request, 'developer_auth/docs_components.html')

def products_overview(request):
    return render(request, 'developer_auth/product/product_overview.html')

def product_create(request):
    return render(request, 'developer_auth/product/product_create.html')

def product_get_all(request):
    return render(request, 'developer_auth/product/product_get_all.html')

def product_get_one(request):
    return render(request, 'developer_auth/product/product_get_one.html')

def product_update(request):
    return render(request, 'developer_auth/product/product_update.html')

def product_delete(request):
    return render(request, 'developer_auth/product/product_delete.html')


def category_overview(request):
    return render(request, 'developer_auth/category/category_overview.html')

def category_create(request):
    return render(request, 'developer_auth/category/category_create.html')

def category_delete(request):
    return render(request, 'developer_auth/category/category_delete.html')

def category_get(request):
    return render(request, 'developer_auth/category/category_get.html')

def category_update(request):
    return render(request, 'developer_auth/category/category_update.html')


def review_overview(request):
    return render(request, 'developer_auth/review/review_overview.html')

def review_create(request):
    return render(request, 'developer_auth/review/review_create.html')

def review_delete(request):
    return render(request, 'developer_auth/review/review_delete.html')

def review_get_all(request):
    return render(request, 'developer_auth/review/review_get_all.html')

def review_get_one(request):
    return render(request, 'developer_auth/review/review_get_one.html')

def review_update(request):
    return render(request, 'developer_auth/review/review_update.html')


def cart_overview(request):
    return render(request, 'developer_auth/cart/cart_overview.html')

def cart_get(request):
    return render(request, 'developer_auth/cart/cart_get.html')

def cart_add(request):
    return render(request, 'developer_auth/cart/cart_add.html')

def cart_increase(request):
    return render(request, 'developer_auth/cart/cart_increase.html')

def cart_decrease(request):
    return render(request, 'developer_auth/cart/cart_decrease.html')

def cart_remove(request):
    return render(request, 'developer_auth/cart/cart_remove.html')


def orders_get_all(request):
    return render(request, 'developer_auth/order/orders_get_all.html')

def orders_get_one(request):
    return render(request, 'developer_auth/order/orders_get_one.html')

def orders_create(request):
    return render(request, 'developer_auth/order/orders_create.html')

def orders_overview(request):
    return render(request, 'developer_auth/order/orders_overview.html')

def orders_cancel(request):
    return render(request, 'developer_auth/order/orders_cancel.html')

def register(request):
    if request.method == 'POST':
        form = DeveloperRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = DeveloperRegisterForm()
    return render(request, 'developer_auth/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = DeveloperLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                developer = authenticate(request, email=email, password=password)
                
                print(developer)    
                if developer is not None:
                    auth_login(request, developer)
                    return redirect('index')
                else:
                    print(f"errors: {form.errors}")
                    print("invalid password")
            except Developer.DoesNotExist:
                print("Devloper not found")
    else:
        form = DeveloperLoginForm()
    return render(request, 'developer_auth/login.html', {'form': form})

def logout(request):
    request.session.flush()
    auth_logout(request)
    return redirect('account_login')

@login_required(login_url='account_login')
def generate_api_key(request):
    if request.method == 'POST':
        user_email = request.user.email
        name = request.POST.get('api_key_name')
        password = request.POST.get('password')
        mode = request.POST.get('mode', 'test')

        # Get the developer instance safely
        developer = get_object_or_404(Developer, email=user_email)

        # Optional: Prevent duplicate API keys for a developer
        # if DeveloperAPIKey.objects.filter(developer=developer).exists():
        #     return JsonResponse({'error': 'Developer already has an API key.'}, status=400)

        # Create an API key for the developer
        authenticated_developer = authenticate(request, email=user_email, password=password)
        if authenticated_developer is None:
            response = JsonResponse({'message': 'error'})
            response['HX-Trigger'] = json.dumps({
                'showToast': {
                'type': 'error',  # or 'warning', 'info'
                'message': 'Authentication failed. Incorrect password.'
            }  # Triggers page reload
            })
            return response
        
        plain_text = f"sk_{mode}_" + secrets.token_urlsafe(48)
        encryted = encrypt_key(plain_text)
        public_key = f"pk_{mode}_" + secrets.token_urlsafe(48)
        # Revoke existing active API keys for the developer before creating a new one.
        revoke = APIKey.objects.filter(
            developer=developer, 
            is_active=True).update(is_active=False, revoked_at=timezone.now())
        key = APIKey.objects.create(
            name=name,
            developer=developer,
            public_key=public_key,
            encrypted_secret_key=encryted,
            mode=mode
        )
        # Return partial template for HTMX updates
        messages.success(request, 'API key created successfully!')
        response = JsonResponse({'message': 'Success'})
        response['HX-Trigger'] = json.dumps({
            'showToast': {'type': 'success', 'message': 'Saved!'},
            'closeModal': True,
            'refreshList': True  # Triggers page reload
        })
    return response

def api_key(request):
    return render(request, 'developer_auth/api_key.html')

@login_required(login_url='account_login')
def regenerate_api_key(request):
    if request.method == 'POST':
        api_key_id = request.data.get('key_id')
        try:
            old_key = APIKey.objects.get(id=api_key_id)
            old_key.revoked_at = timezone.now()
            old_key.is_active = False
            old_key.save()

            new_api_key, full_key = DeveloperAPIKey.objects.create_key(name=old_key.name, developer=old_key.developer)
            return JsonResponse({'API-Key': full_key})
        except DeveloperAPIKey.DoesNotExist:
            return JsonResponse({'error': "API key not found."}, status=404)
    else:
        return redirect('dashboard')

import requests
baseURL = "http://localhost:3000/api/v1"

from django.contrib import messages

def create_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category = request.POST.get('category')
        stock_quantity = request.POST.get('stock_quantity')
        data = {
            'name': name,
            'description': description,
            'price': price,
            'category': category,
            'stock_quantity': stock_quantity
        }
        key = APIKey.objects.filter(developer=request.user, is_active=True).first()
        header = {
            "X-Secret-Key": decrypt_key(key.encrypted_secret_key)
        }
        try:
            response = requests.post(f"{baseURL}/products/create/", json=data, headers=header)
            if response.status_code == 201:
                messages.success(request, 'Product created successfully!')
                django_response = JsonResponse({'message': 'Product created successfully.'}, status=201)
                django_response['HX-Trigger'] = json.dumps({
                    'closeModal': True,
                    'refreshList': True
                })
                return django_response
            else:
                error_msg = response.json().get('detail', 'Failed to create product.')
                django_response = JsonResponse({'error': error_msg}, status=response.status_code)
                django_response['HX-Trigger'] = json.dumps({
                    'showToast': {'type': 'error', 'message': f"Error: {error_msg}"}
                })
                return django_response
        except Exception as e:
            django_response = JsonResponse({'error': str(e)}, status=500)
            django_response['HX-Trigger'] = json.dumps({
                'showToast': {'type': 'error', 'message': 'An unexpected error occurred.'}
            })
            return django_response
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
    
def create_category(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

    name = request.POST.get('name')
    description = request.POST.get('description')

    data = {
        'name': name,
        'description': description
    }

    key = APIKey.objects.filter(developer=request.user, is_active=True).first()

    if not key:
        return JsonResponse({'error': 'No active API key found.'}, status=400)

    headers = {
        "X-Public-Key": key.public_key,
        "X-Secret-Key": decrypt_key(key.encrypted_secret_key),
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            f"{baseURL}/products/categories/all/",
            json=data,
            headers=headers
        )

        if response.status_code == 201:
            django_response = JsonResponse({'message': 'Category created successfully.'}, status=201)
            django_response['HX-Trigger'] = json.dumps({
                'showToast': {'type': 'success', 'message': 'Category created successfully!'},
                'closeModal': True,
                'refreshCategories': True 
            })
            return django_response

        error_msg = response.json().get('detail', 'Failed to create category.')
        django_response = JsonResponse({'error': error_msg}, status=response.status_code)
        django_response['HX-Trigger'] = json.dumps({
            'showToast': {'type': 'error', 'message': f"Error: {error_msg}"}
        })
        return django_response

    except Exception as e:
        django_response = JsonResponse({'error': str(e)}, status=500)
        django_response['HX-Trigger'] = json.dumps({
            'showToast': {'type': 'error', 'message': 'An unexpected error occurred.'}
        })
        return django_response
    
def load_categories(request):
    key = APIKey.objects.filter(developer=request.user, is_active=True).first()

    if not key:
        return JsonResponse({'error': 'No active API key found.'}, status=400)

    headers = {
        "X-Public-Key": key.public_key,
        "X-Secret-Key": decrypt_key(key.encrypted_secret_key),
        "Content-Type": "application/json",
    }
    try:
        response = requests.get(
            f"{baseURL}/products/categories/all/",
            headers=headers
        )

        # if response.status_code == 200:
        #     return JsonResponse(
        #         {'message': 'Category created successfully.'},
        #         status=201
        #     )
        if response.status_code == 200:
            data = response.json()['results']
            selected_id = request.GET.get('selected_id')
            return render(request, "developer_auth/partials/category_options.html", {
                'categories': data,
                'selected_id': str(selected_id) if selected_id else None
            })
    except Exception as e:
        return JsonResponse(
            {
                'error': 'An error occurred while creating the category.',
                'details': str(e)
            },
            status=500
        )

def update_product(request, slug):
    context = {}
    if slug:
        try:
            product = Product.objects.get(slug=slug, developer=request.user)
            context['product'] = product
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found.'}, status=404)
        
    if request.method == 'POST':
        data = {}
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category = request.POST.get('category')
        stock_quantity = request.POST.get('stock_quantity')

        if name:
            data['name'] = name
        if description:
            data['description'] = description
        if price:
            data['price'] = price
        if category:
            data['category'] = category
        if stock_quantity:
            data['stock_quantity'] = stock_quantity
        key = APIKey.objects.filter(developer=request.user, is_active=True).first()
        header = {
            "X-Secret-Key": decrypt_key(key.encrypted_secret_key)
        }
        try:
            response = requests.patch(f"{baseURL}/products/{slug}/update/", json=data, headers=header)
            if response.status_code == 200:
                messages.success(request, 'Product updated successfully!')
                django_response = JsonResponse({'message': 'Product updated successfully.'}, status=200)
                django_response['HX-Trigger'] = json.dumps({
                    'closeModal': True,
                    'refreshList': True
                })
                return django_response
            else:
                error_msg = response.json().get('detail', 'Failed to update product.')
                django_response = JsonResponse({'error': error_msg}, status=response.status_code)
                django_response['HX-Trigger'] = json.dumps({
                    'showToast': {'type': 'error', 'message': f"Error: {error_msg}"}
                })
                return django_response
        except Exception as e:
            django_response = JsonResponse({'error': str(e)}, status=500)
            django_response['HX-Trigger'] = json.dumps({
                'showToast': {'type': 'error', 'message': 'An unexpected error occurred.'}
            })
            return django_response

    return JsonResponse({'error': 'Method not allowed'}, status=405)
    
def get_product_form(request, pk=None):
    context = {}
    if pk:
        product = Product.objects.get(pk=pk, developer=request.user)
        context['product'] = product
        # Fetch product data from your API or DB
        # Example using your API pattern:
        key = APIKey.objects.filter(developer=request.user, is_active=True).first()
        header = {
            "X-Secret-Key": decrypt_key(key.encrypted_secret_key)
        }
        try:
            response = requests.get(f"{baseURL}/products/{pk}/", headers=header)
            if response.status_code == 200:
                context['product'] = response.json()
        except Exception as e:
            print(f"Error fetching product: {e}")
            
    return render(request, 'developer_auth/partials/product_form.html', context)

@login_required(login_url='account_login')
def settings(request):
    profile_form = DeveloperUpdateForm(instance=request.user)
    password_form = DeveloperPasswordChangeForm(user=request.user)

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            profile_form = DeveloperUpdateForm(request.POST, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('settings')
        
        elif 'change_password' in request.POST:
            password_form = DeveloperPasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                # Keep the user logged in after password change
                auth_login(request, request.user)
                messages.success(request, 'Password changed successfully!')
                return redirect('settings')

    return render(request, 'developer_auth/settings.html', {
        'form': profile_form,
        'password_form': password_form
    })

@login_required(login_url='account_login')
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        # Optional: Delete related API keys or data explicitly if needed
        # APIKey.objects.filter(developer=user).delete()
        
        user.delete()
        messages.success(request, 'Your account has been successfully deleted.')
        return redirect('register')
    
    return redirect('settings')
