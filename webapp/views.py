from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout, login as auth_login, authenticate
import requests
from django.contrib.auth.models import User
from products.models import Product, Cart, Order
from django.utils.deprecation import MiddlewareMixin

# Create your views here.

baseURL = 'http://127.0.0.1:8000/api'



# token_manager.py
token = None

def fetch_token():
    global token
    token_endpoint = f"{baseURL}/users/token/"
    login_data = {
        'email': 'seidufarid206@gmail.com',
        'password': '919120$'
    }
    response = requests.post(token_endpoint, data=login_data)
    response_data = response.json()
    token = response_data.get('access')
    return token

def get_token():
    if not token:
        return fetch_token()
    return token

def get_cart_data(token):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{baseURL}/cart/', headers=headers)
    if response.status_code == 200:
        return response.json()  # or return just the data you need
    return None

def get_user_details(token, user_id):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{baseURL}/users/{user_id}/', headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def product_list(request):
    # Fetching products
    response = requests.get(f"{baseURL}/products/")
    data = response.json()
    products = data['results']
    
    # Get cart data if user is logged in
    token = request.session.get('access_token')
    if token:
        cart = get_cart_data(token)  # Using the helper method to fetch cart data
    else:
        cart = None
    
    return render(request, 'webapp/product_list.html', {'products': products, 'cart': cart})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    response = requests.get(f"{baseURL}/products/{product.id}/")
    data = response.json()
    token = request.session.get('access_token')
    
    if token:
        cart = get_cart_data(token)  # Using the helper method to fetch cart data
    else:
        cart = None
    
    return render(request, 'webapp/product_details.html', {'product': data, 'cart': cart})

@login_required(login_url='login')
def cart_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    token = request.session.get('access_token')
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f"{baseURL}/cart/", headers=headers)

    # Check if the request was successful (HTTP status 200)
    if response.status_code == 200:
        try:
            cart_data = response.json()  # Try to parse JSON
        except ValueError as e:
            print(f"Error decoding JSON: {e}")
            print(f"Response content: {response.text}")
            cart_data = {}
    else:
        print(f"Failed to fetch cart: {response.status_code}")
        cart_data = {}

    return render(request, 'webapp/cart.html', {'cart': cart_data})
    #return JsonResponse(cart_data, safe=False)

@login_required(login_url='login')
def add_to_cart(request, slug):
    # Check if user details are present; redirect to login if not
    if not request.session.get('access_token'):
        return redirect('login')

    product = get_object_or_404(Product, slug=slug)
    token = request.session.get('access_token')
    headers = {'Authorization': f'Bearer {token}'}

    # Ensure CSRF token is present
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        

        payload = {'product': product.id, 'quantity': quantity}
        response = requests.post(f"{baseURL}/cart/add/", headers=headers, json=payload)

        if response.status_code == 201:
            messages.success(request, 'Product added to cart')
            return redirect('webapp-cart')
        else:
            messages.error(request, 'Failed to add to cart')
            print(f"Failed to add to cart: {response.content}")
            return render(request, 'webapp/error.html', {'message': response.json()})
    else:
        messages.error(request, 'Invalid request method')
        return redirect('webapp-product-details', slug=slug)
        
def decrease_cart_item(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')

    token = request.session.get('access_token')
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.patch(f"{baseURL}/cart/{product_id}/decrease/", headers=headers)

    if response.status_code == 200 or 204:
        print("OK")
        messages.success(request, 'Cart updated!')
        return redirect('webapp-cart')
    else:
        print(f"Failed to decrease item quantity: {response.content}")
        messages.error(request, 'Failed to update cart.')
        return render(request, 'webapp/error.html', {'message': {response.content}})
    
def increase_cart_item(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')

    token = request.session.get('access_token')
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.patch(f"{baseURL}/cart/{product_id}/increase/", headers=headers)

    if response.status_code == 200:
        print('OK')
        messages.success(request, 'Cart updated!')
        return redirect('webapp-cart')
    else:
        print(f"Failed to increase item quanitity: {response.content}")
        messages.error(request, 'Failed to update cart.')
        return render(request, 'webapp/error.html', {'message': response.content})

def delete_cart_item(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')

    response = requests.get(f"{baseURL}/products/{product_id}/")

    token = request.session.get('access_token')
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.delete(f"{baseURL}/cart/{product_id}/remove/", headers=headers)

    if response.status_code == 204:
        print("Deleted cart item")
        return redirect('webapp-cart')
    else:
        print(f"Failed to delete item: {response.content}")
        return render(request, 'webapp/error.html', {'message': {response.content}})

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        token_endpoint = f"{baseURL}/users/token/"
        login_data = {'email': email, 'password': password}

        response = requests.post(token_endpoint, data=login_data)
        if response.status_code == 200:
            response_data = response.json()
            token = response_data.get('access')
            request.session['access_token'] = token
            
            # Fetch user details with the token
            headers = {'Authorization': f'Bearer {token}'}
            user_details_response = requests.get(f"{baseURL}/users/me/", headers=headers)
            if user_details_response.status_code == 200:
                user_details = user_details_response.json()
                request.session['user_email'] = user_details.get('email')

                user = authenticate(request, username=email, password=password)
                if user is not None:
                    auth_login(request, user)
                    messages.success(request, 'Login Successful')
                    next_url = request.GET.get('next') or request.POST.get('next')
                    return redirect(next_url if next_url else 'webapp')
                else:
                    print("isn't auth")
                    messages.error(request, 'Authentication failed')
                    return redirect('webapp')

            messages.error(request, 'Could not fetch user details')
            return redirect('webapp')
        else:
            if response.status_code == 400:
                messages.error(request, 'Invalid email or password')
            elif response.status_code == 401:
                messages.error(request, 'Unauthorized access')
            else:
                messages.error(request, 'An error occurred. Please try again.')
    return render(request, 'webapp/login.html')


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        register_enpoint = f"{baseURL}/users/create/"
        register_data = {'email': email, 'username': username, 'password': password}

        API_KEY = "-x2IHuqqbYXncf9_yu8eJIaqh1NlDmR_LyRf8nmfsGc"
        headers = {'Authorization': API_KEY}

        response = requests.post(register_enpoint, register_data, headers=headers)

        if response.status_code == 201:
            messages.success(request, 'Registration Successful')
            return redirect('login')
        else:
            messages.error(request, 'Unable to create account')

    return render(request, 'webapp/register.html')

def logout(request):
    request.session.flush()
    auth_logout(request)
    messages.success(request, 'Logout Successful')
    return redirect('login')

def review_list(request, slug):
    product = get_object_or_404(Product, slug=slug)

    response = requests.get(f"{baseURL}/products/{product.id}/reviews/")
    if response.status_code == 200:
        data = response.json()
        reviews = data.get('results', [])
    else:
        reviews = []
    return render(request, 'webapp/review_list.html', {'reviews': reviews})
    #return JsonResponse(reviews, safe=False)
# def revi

def submit_review(request, slug):
    if not request.user.is_authenticated:
        return redirect('login')

    token = request.session.get('access_token')
    product = get_object_or_404(Product, slug=slug)
    headers = {'Authorization': f'Bearer {token}'}

    if request.method == 'POST':
        rating = request.POST.get('rating-2')
        comment = request.POST.get('comment')
        payload = {
                    "product": product.id,
                    "rating": rating,
                    "comment": comment
                }
        response = requests.post(f"{baseURL}/products/{product.id}/reviews/create/", headers=headers, json=payload)

        if response.status_code == 201:
            messages.success(request, "Review created successfully!")
            return redirect('webapp-product-details', slug=product.slug)
        else:
            print(f"Failed to submit review: {response.content}")
            messages.error(request, "Error submitting review.")
            return redirect('submit-review', product.slug)
        
    else:
        return render(request, 'webapp/review.html', {'product': product})
    
def create_order(request):
    if not request.user.is_authenticated:
        return redirect('login')

    token = request.session.get('access_token')
    headers = {'Authorization': f'Bearer {token}'}
    cart = Cart.objects.filter(user=request.user).first()
    
    if not cart:
        return redirect('webapp-cart')

    payload = {
        'cart': cart.id,
    }

    response = requests.post(f"{baseURL}/orders/create/", headers=headers, json=payload)

    if response.status_code == 200:
        return redirect('webapp-orders')
    else: 
        print(f"Erro with order: {response.content}")
        return redirect('webapp-cart')

def order_detail(request, order_id):
    if not request.user.is_authenticated:
        return redirect('login')

    token = request.session.get('access_token')
    headers = {'Authorization': f'Bearer {token}'}

    try:
        response = requests.get(f"{baseURL}/orders/{order_id}/", headers=headers)
        response.raise_for_status()

        order_data = response.json()
        items = order_data['items']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching order data: {e}")
        return  redirect('webapp')
    return render(request, 'webapp/order_detail.html', {'order': order_data, 'items': items})
    #return JsonResponse(order_data, safe=False)

def order_list(request):
    if not request.user.is_authenticated:
        return redirect('login')

    token = request.session.get('access_token')
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        response = requests.get(f"{baseURL}/orders/", headers=headers)
        response.raise_for_status()

        orders_data = response.json()
        orders = orders_data['results']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching orders data: {e}")
        return redirect('webapp')
    return render(request, 'webapp/order_list.html', {'orders': orders})
    #return JsonResponse(orders, safe=False)

def cancel_order(request, order_id):
    if not request.user.is_authenticated:
        return redirect('login')

    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status == 'PENDING':
        order.status = 'CANCELLED'
        order.save()

        for item in order.items.all():
            item.product.stock_quantity += item.quantity
            item.product.save()
        print('Order cancelled successfully')
        return redirect('webapp-orders')
    else:
        print('Order cannot be cancelled')
        return  redirect('webapp-orders')


def search_view(request):
    query = request.GET.get('q')
    max_price = request.GET.get('price_max')
    min_price = request.GET.get('price_min')
    category = request.GET.get('category')
    
    filters = {
        'search': query,
        'category': category,
        'price_min': min_price,
        'price_max': max_price
    }
    
    # Remove empty filter parameters
    filters = {k: v for k, v in filters.items() if v}
    
    response = requests.get(f"{baseURL}/products/", params=filters)
    
    if response.status_code == 200:
        data = response.json()
        products = data.get('results', [])
    else:
        products = []
    
    return render(request, 'webapp/active_search_results.html', {'products': products})


def search_results(request):
    query = request.GET.get('q')
    max_price = request.GET.get('max_price')
    min_price = request.GET.get('min_price')
    category = request.GET.get('category')
    
    filters = {
        'search': query,
        'category': category,
        'min_price': min_price,
        'max_price': max_price
    }
    
    # Remove empty filter parameters
    filters = {k: v for k, v in filters.items() if v}
    
    response = requests.get(f"{baseURL}/products/", params=filters)

    if response.status_code == 200:
        data = response.json()
        products = data.get('results', [])
    else:
        products = []
    return render(request, 'webapp/search_results.html', {'products': products})
