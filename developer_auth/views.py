from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from .models import Developer, DeveloperAPIKey
from .forms import DeveloperRegisterForm, DeveloperLoginForm

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

@login_required(login_url='login')
def dashboard(request):
    developer = request.user
    api_keys = DeveloperAPIKey.objects.filter(developer=developer)

    return render(request, 'developer_auth/dashboard.html', {'api_keys': api_keys})

def revoke_key(request, prefix):
    key = DeveloperAPIKey.objects.get(prefix=prefix)
    key.revoked = True
    key.save()
    return redirect('dashboard')

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
    return redirect('login')

@login_required(login_url='login')
def create_api_key(request):
    if request.method == 'POST':
        user_email = request.user.email
        name = request.POST.get('api_key_name')

        # Get the developer instance safely
        developer = get_object_or_404(Developer, email=user_email)

        # Optional: Prevent duplicate API keys for a developer
        # if DeveloperAPIKey.objects.filter(developer=developer).exists():
        #     return JsonResponse({'error': 'Developer already has an API key.'}, status=400)

        # Create an API key for the developer
        api_key, key = DeveloperAPIKey.objects.create_key(developer=developer, name=name)

        # Return partial template for HTMX updates
        return render(request, 'developer_auth/key.html', {'key': key})
    return redirect('dashboard')

def api_key(request):
    return render(request, 'developer_auth/api_key.html')

@login_required(login_url='login')
def regenerate_api_key(request):
    if request.method == 'POST':
        api_key_id = request.data.get('api_key_id')
        try:
            old_key = DeveloperAPIKey.objects.get(id=api_key_id)
            old_key.revoked = True
            old_key.save()

            new_api_key, full_key = DeveloperAPIKey.objects.create_key(name=old_key.name, developer=old_key.developer)
            return JsonResponse({'API-Key': full_key})
        except DeveloperAPIKey.DoesNotExist:
            return JsonResponse({'error': "API key not found."}, status=404)
    else:
        return redirect('dashboard')
