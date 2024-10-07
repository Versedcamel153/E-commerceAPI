from rest_framework import serializers
from .models import Product, Review, Category, ProductImage, Order, OrderItem, Cart, CartItem

class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for the Review model."""
    
    class Meta:
        model = Review
        fields = ['id', 'product', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at']  # Fields that are not writable


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for the ProductImage model."""
    
    class Meta:
        model = ProductImage
        fields = ['id', 'image_url']  # Fields to serialize


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for the Product model, including nested reviews and images."""
    
    reviews = ReviewSerializer(many=True, read_only=True)  # Nested reviews
    images = ProductImageSerializer(many=True, required=False)  # Nested product images

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


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for the Category model."""
    
    class Meta:
        model = Category
        fields = '__all__'  # Include all fields from the Category model


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for the CartItem model, including product name."""
    
    product_name = serializers.SerializerMethodField()  # Custom field for product name

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'quantity']  # Fields to serialize

    def get_product_name(self, obj):
        """Return the name of the product associated with the cart item."""
        return obj.product.name

    def create(self, validated_data):
        """Override create method to associate cart items with the user's cart."""
        request = self.context.get('request', None)
        if request and hasattr(request, 'user'):
            user = request.user
            cart, created = Cart.objects.get_or_create(user=user)  # Get or create cart for user
            validated_data['cart'] = cart  # Associate cart with the cart item

        # Ensure quantity is present
        if 'quantity' not in validated_data:
            validated_data['quantity'] = 1  # Set a default quantity if not provided

        return super().create(validated_data)  # Call the parent create method


class CartSerializer(serializers.ModelSerializer):
    """Serializer for the Cart model, including nested cart items."""
    
    items = CartItemSerializer(many=True, read_only=True)  # Nested cart items

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'created_at']  # Fields to serialize
        read_only_fields = ['id', 'user', 'created_at']  # Read-only fields


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for the OrderItem model, including product details."""
    
    product = ProductSerializer()  # Nested product details

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']  # Fields to serialize


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for the Order model, including nested order items."""
    
    items = OrderItemSerializer(many=True)  # Nested order items

    class Meta:
        model = Order
        fields = ['id', 'user', 'cart', 'status', 'items']  # Fields to serialize

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