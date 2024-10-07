from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import (
    CreateAPIView, ListAPIView, ListCreateAPIView, 
    RetrieveAPIView, UpdateAPIView, DestroyAPIView, 
    RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView
)
from .models import Product, Review, Category, Order, Cart, CartItem
from .filters import ProductFilter
from .serializers import (
    ProductSerializer, ReviewSerializer, 
    CategorySerializer, OrderSerializer, 
    CartSerializer, CartItemSerializer
)

# Create your views here.

class ProductCreateView(CreateAPIView):
    """View for creating a new product."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

class CustomPagination(PageNumberPagination):
    """Custom pagination class to define page size settings."""
    page_size = 10
    page_size_query_param = 'page_size'  # Allow client to set page size
    max_page_size = 100  # Limit on page size

class ProductListView(ListAPIView):
    """View for listing all products with pagination and filtering."""
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = ProductFilter
    pagination_class = CustomPagination

class ProductDetailView(RetrieveAPIView):
    """View for retrieving details of a specific product."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductUpdateView(UpdateAPIView):
    """View for updating an existing product."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]  # Require authentication

class ProductDeleteView(DestroyAPIView):
    """View for deleting a product."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]  # Require authentication

class ReviewListView(ListAPIView):
    """View for listing all reviews for a specific product."""
    queryset = Review.objects.all().order_by('id')
    serializer_class = ReviewSerializer

    def get_queryset(self):
        """Override to filter reviews by product ID."""
        product_pk = self.kwargs['pk']
        return Review.objects.filter(product_id=product_pk)

class ReviewCreateView(CreateAPIView):
    """View for creating a new review for a specific product."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        """Associate the review with the product and user upon creation."""
        product_pk = self.kwargs['pk']
        product = Product.objects.get(pk=product_pk)
        serializer.save(product=product, user=self.request.user)

class ReviewDetail(RetrieveAPIView):
    """View for retrieving a specific review."""
    queryset = Review.objects.all() 
    serializer_class = ReviewSerializer

    def get_object(self):
        """Override to retrieve review by product and review ID."""
        product_pk = self.kwargs['pk']
        review_pk = self.kwargs['review_pk']
        return Review.objects.get(product_id=product_pk, pk=review_pk)

class ReviewUpdateView(UpdateAPIView):
    """View for updating a specific review."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]  # Require authentication

    def get_object(self):
        """Override to retrieve review by product and review ID for update."""
        product_pk = self.kwargs['pk']
        review_pk = self.kwargs['review_pk']
        return Review.objects.get(product_id=product_pk, pk=review_pk)

class ReviewDeleteView(DestroyAPIView):
    """View for deleting a specific review."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]  # Require authentication

    def get_object(self):
        """Override to retrieve review by product and review ID for deletion."""
        product_pk = self.kwargs['pk']
        review_pk = self.kwargs['review_pk']
        return Review.objects.get(product_id=product_pk, pk=review_pk)

class CategoryListCreateView(ListCreateAPIView):
    """View for listing all categories and creating a new category."""
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer

class CategoryRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """View for retrieving, updating, and deleting a specific category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class OrderListView(ListAPIView):
    """View for listing all orders."""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderCreateView(CreateAPIView):
    """View for creating a new order."""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Create an order associated with the user's cart."""
        user = self.request.user
        
        # Get or create the cart for the user
        cart, created = Cart.objects.get_or_create(user=user)

        # Create the order and associate it with the cart
        order = serializer.save(user=user, cart=cart)

        # Add items from the cart to the order (assuming you have a relation defined)
        for item in cart.items.all():
            # Here, you need to create OrderItem instances if not done in the serializer
            order.items.create(product=item.product, quantity=item.quantity)

        # Clear the cart after creating the order
        cart.items.all().delete()

class OrderDetailView(RetrieveUpdateAPIView):
    """View for retrieving and updating a specific order."""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # permission_classes = [IsAuthenticated]  # Uncomment to require authentication

    def get_queryset(self):
        """Override to filter orders by the authenticated user."""
        return self.queryset.filter(user=self.request.user)

class CartDetailView(RetrieveUpdateAPIView):
    """View for retrieving and updating the user's cart."""
    serializer_class = CartSerializer

    def get_object(self):
        """Retrieve the cart associated with the authenticated user."""
        user = self.request.user
        return Cart.objects.get(user=user)

class AddToCartView(APIView):
    """View for adding a product to the user's cart."""
    def post(self, request):
        user = request.user

        # Get or create the user's cart
        cart, created = Cart.objects.get_or_create(user=user)

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
    
    def patch(self, request, *args, **kwargs):
        item_id = kwargs.get('pk')
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