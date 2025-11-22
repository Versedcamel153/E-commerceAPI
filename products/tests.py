# tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Product, Review, Category, Order, Cart, CartItem, User

class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product', price=10.0, stock_quantity=100, category=self.category
        )
    
    def test_create_product(self):
        url = reverse('product-create')
        data = {
            'name': 'New Product',
            'description': 'A new added test product',
            'images': [],
            'price': 20.0,
            'stock_quantity': 50,
            'category': self.category.id
        }
        # Example of creating a product
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_products(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_product(self):
        url = reverse('product-detail', kwargs={'pk': self.product.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_product(self):
        url = reverse('product-update', kwargs={'pk': self.product.id})
        data = {'name': 'Updated Product'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_product(self):
        url = reverse('product-delete', kwargs={'pk': self.product.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ReviewAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product', price=10.0, stock_quantity=100, category=self.category
        )
        self.review = Review.objects.create(product=self.product, user=self.user, rating=5, comment='Great product!')

    def test_create_review(self):
        url = reverse('review-create', kwargs={'pk': self.product.id})
        data = {
            'product' : self.product.id,
            'rating': 5,
            'comment': 'Good product',
            
            }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_reviews(self):
        url = reverse('review-list', kwargs={'pk': self.product.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_review(self):
        url = reverse('review-detail', kwargs={'pk': self.product.id, 'review_pk': self.review.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_review(self):
        url = reverse('review-update', kwargs={'pk': self.product.id, 'review_pk': self.review.id})
        data = {'comment': 'Updated comment'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_review(self):
        url = reverse('review-delete', kwargs={'pk': self.product.id, 'review_pk': self.review.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    

class CategoryAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Test Category')

    def test_create_category(self):
        url = reverse('category-list-create')
        data = {'name': 'New Category'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_categories(self):
        url = reverse('category-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_category(self):
        url = reverse('category-detail', kwargs={'pk': self.category.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_category(self):
        url = reverse('category-detail', kwargs={'pk': self.category.id})
        data = {'name': 'Updated Category'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_category(self):
        url = reverse('category-detail', kwargs={'pk': self.category.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class OrderAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product', price=10.0, stock_quantity=100, category=self.category
        )
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(user=self.user)

    def test_create_order(self):
        url = reverse('order-create')
        data = {
            "cart": self.cart.id,
            "user": self.user.id,
            "items": [],
            'status': 'PENDING'
            }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_order(self):
        order = Order.objects.create(user=self.user, cart=self.cart, status='Pending')
        url = reverse('order-detail', kwargs={'pk': order.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class CartAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product', price=10.0, stock_quantity=100, category=self.category
        )
        self.cart = Cart.objects.create(user=self.user)

    def test_retrieve_cart(self):
        url = reverse('cart-detail')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_to_cart(self):
        url = reverse('cart-item-create')
        data = {'product': self.product.id, 'quantity': 2}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.cart.items.count(), 1)

    def test_remove_cart_item(self):
        cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
        url = reverse('remove-cart-item', kwargs={'pk': cart_item.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_decrease_cart_item_quantity(self):
        cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)
        url = reverse('decrease-cart-item-quantity', kwargs={'pk': cart_item.id})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 1)

    def test_decrease_cart_item_quantity_to_zero(self):
        cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
        url = reverse('decrease-cart-item-quantity', kwargs={'pk': cart_item.id})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(CartItem.DoesNotExist):
            cart_item.refresh_from_db()