from rest_framework import serializers
from .models import Product, Review, Category, ProductImage, Order, OrderItem, Cart, CartItem
from django.db.models import Avg

class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for the Review model."""

    created_at = serializers.DateTimeField(format='%d %B %Y', read_only=True)
    
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['id', 'created_at', ]  # Fields that are not writable
        

class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for the ProductImage model."""
    
    class Meta:
        model = ProductImage
        fields = ['id', 'image_url', 'product']  # Fields to serialize


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for the Product model, including nested reviews and images."""
    
    reviews = ReviewSerializer(many=True, read_only=True)  # Nested reviews
    images = ProductImageSerializer(many=True, required=False)  # Nested product images
    category_name = serializers.ReadOnlyField(source='category.slug')  # Custom field for category name
    average_rating = serializers.ReadOnlyField()
    total_reviews = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'  # Include all fields from the Product model

    def create(self, validated_data):
        """Override the create method to handle nested images."""
        images_data = validated_data.pop('images', [])  # Extract images data
        product = Product.objects.create(**validated_data)  # Create the product instance

        # Create ProductImage instances for each image
        for image_data in images_data:
            ProductImage.objects.create(product=product, **image_data)
        return product
    
    def get_total_reviews(self, obj):
        return obj.reviews.count()


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for the Category model."""
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']  # Include all fields from the Category model


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for the CartItem model, including product name."""
    
    product_name = serializers.SerializerMethodField()  # Custom field for product name
    price = serializers.IntegerField(source='product.price', read_only=True)
    slug = serializers.CharField(source='product.slug', read_only=True)
    total_price = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()  # Get images through product relationship

    class Meta:
        model = CartItem
        fields = '__all__'  # Fields to serialize

    def get_total_price(self, obj):
        return obj.get_total_price()

    def get_product_name(self, obj):
        """Return the name of the product associated with the cart item."""
        return obj.product.name

    def get_images(self, obj):
        """Return the images of the product associated with the cart item."""
        return ProductImageSerializer(obj.product.images.all(), many=True).data

    def create(self, validated_data):
        """Override create method to associate cart items with the correct cart."""
        request = self.context.get('request')  # Get the user_id from the context
        if request:
            user_id = self.request.query_params.get('user_id')  # Expecting `user_id` to be passed in the request data
            if not user_id:
                raise serializers.ValidationError({"user_id": "This field is required."})

            # Ensure the `user_id` has a cart or create one
            cart, created = Cart.objects.get_or_create(user_id=user_id)
            validated_data['cart'] = cart

        # Ensure quantity is present
        if 'quantity' not in validated_data:
            validated_data['quantity'] = 1  # Set a default quantity if not provided

        return super().create(validated_data)

class CartSerializer(serializers.ModelSerializer):
    """Serializer for the Cart model, including nested cart items."""
    
    items = CartItemSerializer(many=True, read_only=True)  # Nested cart items
    total_quantity = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = '__all__'  # Fields to serialize
        read_only_fields = ['id', 'user_id', 'created_at']  # Read-only fields
    
    def get_total_quantity(self, obj):
        return obj.total_quantity()
    
    def get_total_price(self, obj):
        return obj.total_price


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for the OrderItem model, including product details."""
    
    product = ProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']  # Fields to serialize


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for the Order model, including nested order items."""
    
    items = OrderItemSerializer(many=True)  # Nested order items
    item_count = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format='%d %B %Y', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'  # Fields to serialize

    def get_item_count(self, obj):
        return obj.items.count()

    def create(self, validated_data):
        """Override the create method to handle order items and stock management."""
        order_items = validated_data.pop('items', [])  # Extract order items
        order = Order.objects.create(**validated_data)  # Create the order instance

        # Loop through order items to manage stock and create OrderItem instances
        for item_data in order_items:
            product = item_data['product']
            quantity = item_data['quantity']

            # Check stock availability
            if quantity > product.stock_quantity:
                raise serializers.ValidationError(f"Insufficient stock for product {product.name}.")

            product.stock_quantity -= quantity  # Deduct quantity from stock
            product.save()  # Save the updated product stock

            OrderItem.objects.create(order=order, product=product, quantity=quantity)  # Create OrderItem

        return order  # Return the created order