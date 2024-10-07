import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    """Filter set for filtering products based on various criteria."""
    
    name = django_filters.CharFilter(lookup_expr='icontains')  # Filter by name (case insensitive)
    description = django_filters.CharFilter(lookup_expr='icontains')  # Filter by description (case insensitive)
    category = django_filters.CharFilter(lookup_expr='exact')  # Filter by exact category
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')  # Minimum price
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')  # Maximum price
    stock_quantity = django_filters.BooleanFilter(field_name='stock_quantity', method='filter_stock')  # Filter by stock availability

    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price_min', 'price_max', 'stock_quantity']

    def filter_stock(self, queryset, name, value):
        """Filter the queryset based on stock availability."""
        if value:
            return queryset.filter(stock_quantity__gt=0)  # Filter for products in stock
        return queryset  # Return all products if stock filter is not applied