from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError, AuthenticationFailed, PermissionDenied
from rest_framework.generics import (
    CreateAPIView, ListAPIView, ListCreateAPIView, 
    RetrieveAPIView, UpdateAPIView, DestroyAPIView, 
    RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView
)
from rest_framework_api_key.permissions import BaseHasAPIKey
from rest_framework import serializers
from developer_auth.models import DeveloperAPIKey as APIKey
from .models import Product, Review, Category, Order, Cart, CartItem, OrderItem, ProductImage as Image
from .filters import ProductFilter
from .serializers import (
    ProductSerializer, ReviewSerializer, 
    CategorySerializer, OrderSerializer, 
    ProductImageSerializer, CartSerializer,
)

# Create your views here.

# class GenerateAPIKeyView(APIView):
#     """View for generating an API key for the authenticated user."""
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         """Generate an API key for the authenticated user."""
#         user = self.request.user
#         if user.role != 'developer':
#             return Response({"error": "Only developers can generate API keys."},
#                             status=status.HTTP_403_FORBIDDEN)
#         # Check if user already has an API key
#         if APIKey.objects.filter(name=user.username).exists():
#             return Response({"error": "API key already exists for this user."}, 
#                             status=status.HTTP_400_BAD_REQUEST)
            
#         # Create new API key
#         api_key, key = APIKey.objects.create_key(name='')
#         return Response({"api_key": key}, status=status.HTTP_201_CREATED)
        
class HasAPIKeyView(BaseHasAPIKey):
    """
    Custom permission to check if the request contains a valid API key.
    """
    model = APIKey

    def get_key(self, request):
        api_key = request.headers.get('API-KEY')
        if not api_key:
            raise AuthenticationFailed("Missing API key in 'API-KEY' header.")
        return api_key
        
class ProductCreateView(CreateAPIView):
    """View for creating a new product."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [HasAPIKeyView]  # Require authentication 

class ProductListView(ListAPIView):
    """View for listing all products with pagination and filtering."""
    serializer_class = ProductSerializer
    permission_classes = [HasAPIKeyView]  # Require authentication
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = ProductFilter
    search_fields = ['name', 'description']

    def get_queryset(self):
        api_key = self.request.headers.get('API-KEY')

        if not api_key:
            raise PermissionDenied("Invalid API Key.")
        
        try:
            api_key_obj = APIKey.objects.get_from_key(api_key)
            print("API Key is valid!")
        except APIKey.DoesNotExist:
            print("Invalid API Key!")
        
        developer = api_key_obj.developer
        return Product.objects.filter(developer=developer)


    def get_object(self):
        return super().get_object()

class ProductDetailView(RetrieveAPIView):
    """View for retrieving details of a specific product."""
    queryset = Product.objects.all()
    permission_classes = [HasAPIKeyView]  # Require authentication
    serializer_class = ProductSerializer
    lookup_field = 'slug'

class ProductUpdateView(UpdateAPIView):
    """View for updating an existing product."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [HasAPIKeyView]  # Require authentication

class ProductDeleteView(DestroyAPIView):
    """View for deleting a product."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [HasAPIKeyView]  # Require authentication

class ProductImage(CreateAPIView):
    serializer_class = ProductImageSerializer
    queryset = Image
    permission_classes = [HasAPIKeyView]

class ProductImageList(ListAPIView):
    serializer_class= ProductImageSerializer
    permission_classes = [HasAPIKeyView]

    def get_queryset(self):
        api_key = self.request.headers.get('API-KEY')

        if not api_key:
            raise PermissionDenied("Invalid API Key.")
        
        try:
            api_key_obj = APIKey.objects.get_from_key(api_key)
            print("API Key is valid!")
        except APIKey.DoesNotExist:
            print("Invalid API Key!")
        
        developer = api_key_obj.developer
        return Image.objects.filter(product__developer=developer)

class ProductImageUpdate(UpdateAPIView):
    serializer_class = ProductImageSerializer
    permission_classes = [HasAPIKeyView]

    def get_queryset(self):
        api_key = self.request.headers.get('API-KEY')

        if not api_key:
            raise PermissionDenied("Invalid API Key.")
        
        try:
            api_key_obj = APIKey.objects.get_from_key(api_key)
            print("API Key is valid!")
        except APIKey.DoesNotExist:
            print("Invalid API Key!")
        
        developer = api_key_obj.developer
        return Image.objects.filter(product__developer=developer)
    
class ProductImageDetails(RetrieveAPIView):
    serializer_class = ProductImageSerializer
    permission_classes = [HasAPIKeyView]

    def get_queryset(self):
        api_key = self.request.headers.get('API-KEY')

        if not api_key:
            raise PermissionDenied("Invalid API Key.")
        
        try:
            api_key_obj = APIKey.objects.get_from_key(api_key)
            print("API Key is valid!")
        except APIKey.DoesNotExist:
            print("Invalid API Key!")
        
        developer = api_key_obj.developer
        return Image.objects.filter(product__developer=developer)

class ProductImageDelete(DestroyAPIView):
    serializer_class = ProductImageSerializer

    def get_queryset(self):
        #api_key = self.request.headers.get('API-KEY')

        # if not api_key:
        #     raise PermissionDenied("Invalid API Key.")
        api_key = 'KyHmZQhB.78g0PuYQ1IJ9YicQ8v6lAfZMeE8UdBy2'
        try:
            api_key_obj = APIKey.objects.get_from_key(api_key)
            print("API Key is valid!")
        except APIKey.DoesNotExist:
            print("Invalid API Key!")
        
        developer = api_key_obj.developer
        return Image.objects.filter(product__developer=developer)


class ReviewListView(ListAPIView):
    """View for listing all reviews for a specific product."""
    queryset = Review.objects.all().order_by('id')
    serializer_class = ReviewSerializer
    lookup_field = 'slug'
    permission_classes = [HasAPIKeyView]  # Require authentication

    def get_queryset(self):
        """Override to filter reviews by product ID."""
        slug = self.kwargs['slug']
        product = get_object_or_404(Product, slug=slug)

        return Review.objects.filter(product_id=product.pk)

class ReviewCreateView(CreateAPIView):
    """View for creating a new review for a specific product."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'slug'
    permission_classes = [HasAPIKeyView]  # Require authentication

    def perform_create(self, serializer):
        """Associate the review with the product and user upon creation."""
        slug = self.kwargs['slug']
        product = get_object_or_404(Product, slug=slug)

        serializer.save(product=product)
        
class ReviewDetail(RetrieveAPIView):
    """View for retrieving a specific review."""
    queryset = Review.objects.all() 
    serializer_class = ReviewSerializer
    lookup_field = 'slug'
    permission_classes = [HasAPIKeyView]  # Require authentication

    def get_object(self):
        """Override to retrieve review by product and review ID."""
        slug = self.kwargs['slug']
        review_pk = self.kwargs['review_pk']
        product = get_object_or_404(Product, slug=slug)

        return Review.objects.get(product_id=product.pk, pk=review_pk)

class ReviewUpdateView(UpdateAPIView):
    """View for updating a specific review."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'slug'
    permission_classes = [HasAPIKeyView]  # Require authentication

    def get_object(self):
        """Override to retrieve review by product and review ID for update."""
        slug = self.kwargs['slug']
        review_pk = self.kwargs['review_pk']
        product = get_object_or_404(Product, slug=slug)

        return Review.objects.get(product_id=product.pk, pk=review_pk)

class ReviewDeleteView(DestroyAPIView):
    """View for deleting a specific review."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [HasAPIKeyView]  # Require authentication
    lookup_field = 'slug'

    def get_object(self):
        """Override to retrieve review by product and review ID for deletion."""
        slug = self.kwargs['slug']
        product = get_object_or_404(Product, slug=slug)
        review_pk = self.kwargs['review_pk']
        
        return Review.objects.get(product_id=product.pk, pk=review_pk)

class CategoryListCreateView(ListCreateAPIView):
    """View for listing all categories and creating a new category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [HasAPIKeyView]  # Require authentication

    def get_queryset(self):
        api_key = self.request.headers.get('API-KEY')
        if not api_key:
            raise PermissionDenied("API Key is required.")
        
        try:
            api_key_obj = APIKey.objects.get_from_key(api_key)
        except APIKey.DoesNotExist:
            raise ValidationError("Invalid API Key.")
        
        developer = api_key_obj.developer
        return Category.objects.filter(developer=developer)

class CategoryRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """View for retrieving, updating, and deleting a specific category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [HasAPIKeyView]  # Require authentication

class OrderListView(ListAPIView):
    """View for listing orders for the authenticated user."""
    serializer_class = OrderSerializer
    permission_classes = [HasAPIKeyView]  # Require authentication

    def get_queryset(self):
        """Override to filter orders by API Key and user ID."""
        api_key = self.request.headers.get("API-KEY")
        if not api_key:
            raise PermissionDenied("API Key is required.")
        
        try:
            api_key_obj = APIKey.objects.get_from_key(api_key)
        except APIKey.DoesNotExist:
            raise ValidationError("Invalid API Key.")
        
        developer = api_key_obj.developer

        user_id = self.request.query_params.get('user_id')
        if not user_id:
            raise ValidationError("User ID is required.")
        
        return Order.objects.filter(user_id=user_id, developer=developer)


class OrderCreateView(CreateAPIView):
    """View for creating a new order."""
    serializer_class = OrderSerializer
    permission_classes = [HasAPIKeyView] # Require authentication


    def post(self, request, *args, **kwargs):
        """Create an order and associate it with the user's cart."""
        user_id = self.request.query_params.get('user_id')
        print(f'User ID: {user_id}')
        
        # Get or create the cart for the user
        cart, created = Cart.objects.get_or_create(user_id=user_id)
        print(f'Cart: {cart}')

        # Ensure the cart isn't empty
        if not cart.items.exists():
            raise ValidationError("Your cart is empty.")

        api_key = self.request.headers.get("API-KEY")
        if not api_key:
            raise PermissionDenied("API Key is required.")
        
        try:
            api_key_obj = APIKey.objects.get_from_key(api_key)
        except APIKey.DoesNotExist:
            raise ValidationError("Invalid API Key.")
        
        developer = api_key_obj.developer
        print(f"Developer: {developer}")

        # Create the order and associate it with the cart
        order = Order.objects.create(user_id=user_id, cart=cart, developer=developer)

        # Aggregate cart items and add them to the order
        for cart_item in cart.items.all():
            product = cart_item.product
            quantity = cart_item.quantity

            if product.stock_quantity < quantity:
                raise ValidationError(f"Out of stock for {product.name}")
            product.stock_quantity -= quantity 
            product.save()

            # Check if this product already exists in the order
            existing_order_item = OrderItem.objects.filter(order=order, product=product).first()

            if existing_order_item:
                # If the product is already in the order, update the quantity
                existing_order_item.quantity += quantity
                existing_order_item.save()
            else:
                # Otherwise, create a new OrderItem for this product
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity
                )

        # Optionally: Clear the cart after creating the order
        cart.items.all().delete()

        # Return the created order response
        return Response({
            "message": "Order created successfully.",
            "order_id": order.id,
            "total_price": order.total_price,
        })
    
class OrderCancelAPIView(UpdateAPIView):
    """API endpoint to cancel an order and restore stock."""
    permission_classes = [HasAPIKeyView]  # Require authentication
    
    def patch(self, request, pk):
        """Cancel the order and restore stock."""
        try:
            order = Order.objects.get(pk=pk, user_id=self.request.query_params.get('user_id'))
        except Order.DoesNotExist:
            return Response({'detail': 'Order not found or not associated with this user.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the order is already canceled or completed
        if order.status in [Order.Status.CANCELLED, Order.Status.COMPLETED]:
            return Response({'detail': 'Order cannot be canceled as it is already completed or canceled.'}, status=status.HTTP_400_BAD_REQUEST)

        # Update the order status to canceled
        order.status = Order.Status.CANCELLED
        order.save()

        # Restore stock for the canceled order's items
        for order_item in order.items.all():
            product = order_item.product
            product.stock_quantity += order_item.quantity
            product.save()

        # Return the updated order information
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderDetailView(RetrieveAPIView):
    """View for retrieving and updating a specific order."""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [HasAPIKeyView]  # require authentication

    def get_queryset(self):
        """Override to filter orders by the authenticated user."""
        user_id = self.request.query_params.get('user_id')
        return self.queryset.filter(user_id=user_id)

class CartDetailView(RetrieveUpdateAPIView):
    """View for retrieving and updating the user's cart."""
    serializer_class = CartSerializer
    permission_classes = [HasAPIKeyView]  # Require authentication

    def get_object(self):
        """Retrieve the cart associated with the authenticated user."""
        #print(f'User: {self.request.user.is_authenticated}')
        user_id = self.request.query_params.get('user_id')
        #print(f'User ID: {user_id}')
        if not user_id:
            raise serializers.ValidationError({'user_id': "User ID is required."})
        cart, created = Cart.objects.get_or_create(user_id=user_id)
        return cart

class AddToCartView(APIView):
    """View for adding a product to the user's cart."""
    permission_classes = [HasAPIKeyView] # Require authentication

    def post(self, request):
        user_id = self.request.query_params.get('user_id')
        print(f'User ID: {user_id}')

        # Get or create the user's cart
        cart, created = Cart.objects.get_or_create(user_id=user_id)

        product_id = request.data.get('product')
        quantity = request.data.get('quantity', 1)  # Default to 1 if not provided

        if not product_id:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the item already exists in the cart
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not item_created:
            # If the item already exists, increase the quantity
            cart_item.quantity += int(quantity)
        else:
            # If it's a new item, set the quantity
            cart_item.quantity = int(quantity) if quantity is not None else 1  # Ensure quantity is set

        cart_item.save()  # Save the cart item with the updated quantity

        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)

class RemoveCartItemView(DestroyAPIView):
    """View for removing a specific item from the cart."""
    queryset = CartItem.objects.all()
    permission_classes = [HasAPIKeyView] # Require authentication

    def delete(self, request, *args, **kwargs):
        item_id = kwargs.get('pk')
        try:
            item = self.get_object()
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class DecreaseCartItemQuantityView(UpdateAPIView):
    """View for decreasing the quantity of a specific item in the cart."""
    queryset = CartItem.objects.all()
    permission_classes = [HasAPIKeyView] # Require authentication
    
    def patch(self, request, *args, **kwargs):
        try:
            item = self.get_object()
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
                return Response({"quantity": item.quantity}, status=status.HTTP_200_OK)
            else:
                # Optionally remove the item if quantity reaches zero
                item.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class IncreaseCartItemQuantityView(UpdateAPIView):
    """View for increasing the quantity of a specific item in the cart."""
    queryset = CartItem.objects.all()
    permission_classes = [HasAPIKeyView] # Require authentication

    def patch(self, request, *args, **kwargs):
        try:
            item = self.get_object()
            item.quantity += 1
            item.save()
            return Response({"quantity": item.quantity}, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)