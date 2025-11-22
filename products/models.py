from django.db import models
from django.db.models import Avg
from django.contrib.auth import get_user_model
from django.utils.text import slugify
import decimal as Decimal
from developer_auth.models import Developer

User = get_user_model()

class Category(models.Model):
    """Model representing a product category."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, related_name='developer_category')


    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        """Return the string representation of the category."""
        return self.name
    

class Product(models.Model):
    """Model representing a product in the inventory."""
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    stock_quantity = models.PositiveIntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, related_name='developer_products')

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
           return reviews.aggregate(average_rating=Avg('rating'))['average_rating']
        return 0

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        """Return the string representation of the product."""
        return self.name
    

class ProductImage(models.Model):
    """Model representing an image associated with a product."""
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image_url = models.URLField(max_length=250, unique=True)

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
    user_id = models.PositiveIntegerField() # External user id from developer's web app.
    username = models.CharField(max_length=100, default='Anonymous')
    rating = models.IntegerField(choices=Rating.choices)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['product', 'user_id']

    def __str__(self):
        """Return the string representation of the review."""
        return f"{self.product.name} - {self.user_id} - {self.rating}"


class Cart(models.Model):
    """Model representing a shopping cart for a user."""
    user_id = models.PositiveIntegerField(unique=True) # External user id from developer's web app.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the string representation of the cart."""
        return f"Cart for User: {self.user_id}"

    def total_quantity(self):
        return sum(item.quantity for item in self.items.all())
    
    @property
    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.items.all())
    



class CartItem(models.Model):
    """Model representing an item in a user's cart."""
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        """Return the string representation of the cart item."""
        return f"{self.product.name} - {self.quantity} in cart"
    
    def get_total_price(self):
        return self.product.price * self.quantity



class Order(models.Model):
    """Model representing a user's order."""
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        CANCELLED = 'CANCELLED', 'Cancelled'
        COMPLETED = 'COMPLETED', 'Completed'

    user_id = models.PositiveIntegerField() # External user id from developer's web app.
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, related_name='developer_orders')


    def __str__(self):
        """Return the string representation of the order."""
        return f"Order {self.id} by User: {self.user_id}"
    
    def save(self, *args, **kwargs):
        """Override save method to set the total price from the cart."""
        
        if not self.total_price:
            self.total_price = self.cart.total_price
        super().save(*args, **kwargs)
    

class OrderItem(models.Model):
    """Model representing an item in an order."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        """Return the string representation of the order item."""
        return f"{self.product.name} - {self.quantity} in order"