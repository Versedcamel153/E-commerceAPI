from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    """Model representing a product category."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        """Return the string representation of the category."""
        return self.name
    

class Product(models.Model):
    """Model representing a product in the inventory."""
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    stock_quantity = models.PositiveIntegerField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the string representation of the product."""
        return self.name
    

class ProductImage(models.Model):
    """Model representing an image associated with a product."""
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image_url = models.ImageField(upload_to='product_images/')

    def __str__(self):
        """Return the string representation of the product image."""
        return f"Image for {self.product.name}"


class Review(models.Model):
    """Model representing a review for a product."""
    class Rating(models.IntegerChoices):
        ONE = 1, '1 Star'
        TWO = 2, '2 Stars'
        THREE = 3, '3 Stars'
        FOUR = 4, '4 Stars'
        FIVE = 5, '5 Stars'

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=Rating.choices)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['product', 'user']

    def __str__(self):
        """Return the string representation of the review."""
        return f"{self.product.name} - {self.user.username} - {self.rating}"


class Cart(models.Model):
    """Model representing a shopping cart for a user."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the string representation of the cart."""
        return f"Cart for {self.user.username}"


class CartItem(models.Model):
    """Model representing an item in a user's cart."""
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        """Return the string representation of the cart item."""
        return f"{self.product.name} - {self.quantity} in cart"


class Order(models.Model):
    """Model representing a user's order."""
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        CANCELLLED = 'CANCELLED', 'Cancelled'
        COMPLETED = 'COMPLETED', 'Completed'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    def __str__(self):
        """Return the string representation of the order."""
        return f"Order {self.id} by {self.user.username}"
    

class OrderItem(models.Model):
    """Model representing an item in an order."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        """Return the string representation of the order item."""
        return f"{self.product.name} - {self.quantity} in order"