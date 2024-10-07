from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ReviewCreateView, 
    ReviewDeleteView,
    ReviewUpdateView, 
    ReviewDetail,
    ReviewListView,
    CategoryListCreateView, 
    CategoryRetrieveUpdateDestroyView,
    OrderCreateView,
    OrderDetailView,
    CartDetailView,
    AddToCartView,
    RemoveCartItemView,
    DecreaseCartItemQuantityView,
    OrderListView,
)

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),  # GET all products
    path('products/create/', ProductCreateView.as_view(), name='product-create'),  # POST create product
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),  # GET a specific product
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),  # PUT update product
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),  # DELETE product
    path('products/<int:pk>/reviews/create/', ReviewCreateView.as_view(), name='review-create'),
    path('products/<int:pk>/reviews/<int:review_pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),
    path('products/<int:pk>/reviews/<int:review_pk>/update/', ReviewUpdateView.as_view(), name='review-update'),
    path('products/<int:pk>/reviews/<int:review_pk>/', ReviewDetail.as_view(), name='review-detail'),
    path('products/<int:pk>/reviews/', ReviewListView.as_view(), name='review-list'),
    path('products/categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('products/categories/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-detail'),
    path('orders/', OrderListView.as_view(), name='order-list' ),
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('cart/', CartDetailView.as_view(), name='cart-detail'),
    path('cart/add/', AddToCartView.as_view(), name='cart-item-create'),
    path('cart/<int:pk>/remove/', RemoveCartItemView.as_view(), name='remove-cart-item'),
    path('cart/<int:pk>/decrease/', DecreaseCartItemQuantityView.as_view(), name='decrease-cart-item-quantity'),
]
