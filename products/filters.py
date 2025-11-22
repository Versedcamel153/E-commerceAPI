import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    """Filter set for filtering products based on various criteria."""
    
    name = django_filters.CharFilter(lookup_expr='icontains')  # Filter by name (case insensitive)
    slug = django_filters.CharFilter(field_name='slug',lookup_expr='icontains' )
    description = django_filters.CharFilter(lookup_expr='icontains')  # Filter by description (case insensitive)
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')  # Filter by exact category
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')  # Minimum price
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')  # Maximum price
    stock_quantity = django_filters.BooleanFilter(field_name='stock_quantity', method='filter_stock')  # Filter by stock availability

    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'min_price', 'max_price', 'stock_quantity']

    def filter_stock(self, queryset, name, value):
        """Filter the queryset based on stock availability."""
        if value:
            return queryset.filter(stock_quantity__gt=0)  # Filter for products in stock
        return queryset  # Return all products if stock filter is not applied