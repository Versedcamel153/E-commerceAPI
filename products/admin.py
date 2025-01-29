from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Product, Category, ProductImage, Review, Cart, CartItem, Order, OrderItem
from .resources import ProductResource

# Register your models here.
admin.site.register(Category)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ProductResource
    list_display = ('name', 'slug', 'stock_quantity','price')
    inlines = [ProductImageInline, ReviewInline]

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_url')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user_id', 'rating')

@admin.register(CartItem)
class CartItem(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')

@admin.register(Cart)
class Cart(admin.ModelAdmin):
    list_display = ('user_id', 'created_at')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ('product', 'quantity')
    show_change_link = True

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'developer', 'user_id', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at', 'developer', 'user_id')
    search_fields = ('user__username', 'id')
    inlines = [OrderItemInline]
    readonly_fields = ('created_at', 'total_price')

    def total_price(self, obj):
        return obj.total_price
    total_price.short_description = 'Total Price'

    actions = ['mark_as_shipped']

    def mark_as_shipped(self, request, queryset):
        queryset.update(status=Order.Status.SHIPPED)
        self.message_user(request, "Selected orders have been marked as shipped.")
    mark_as_shipped.short_description = 'Mark selected orders as shipped'

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)