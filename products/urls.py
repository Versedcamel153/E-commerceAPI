from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
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
    IncreaseCartItemQuantityView,
    OrderCancelAPIView,
    ProductImage,
    ProductImageList,
    ProductImageUpdate,
    ProductImageDelete,
    ProductImageDetails,
)

urlpatterns = [
    path('images/create/', ProductImage.as_view(), name='image-create'),
    path('images/', ProductImageList.as_view(), name='images'),
    path('images/<int:pk>/update/', ProductImageUpdate.as_view(), name='images-update'),
    path('images/<int:pk>/', ProductImageDetails.as_view(), name='images-details'),
    path('images/<int:pk>/delete/', ProductImageDelete.as_view(), name='images-delete'),
    path('products/', ProductListView.as_view(), name='product-list'),  # GET all products
    path('products/create/', ProductCreateView.as_view(), name='product-create'),  # POST create product
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),  # GET a specific product
    path('products/<slug:slug>/update/', ProductUpdateView.as_view(), name='product-update'),  # PUT update product
    path('products/<slug:slug>/delete/', ProductDeleteView.as_view(), name='product-delete'),  # DELETE product
    path('products/<slug:slug>/reviews/create/', ReviewCreateView.as_view(), name='review-create'),
    path('products/<slug:slug>/reviews/<int:review_pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),
    path('products/<slug:slug>/reviews/<int:review_pk>/update/', ReviewUpdateView.as_view(), name='review-update'),
    path('products/<slug:slug>/reviews/<int:review_pk>/', ReviewDetail.as_view(), name='review-detail'),
    path('products/<slug:slug>/reviews/', ReviewListView.as_view(), name='review-list'),
    path('products/categories/all/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('products/categories/<slug:slug>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-detail'),
    path('orders/', OrderListView.as_view(), name='order-list' ),
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),
    path('orders/<int:pk>/cancel/', OrderCancelAPIView.as_view(), name='order-cancel'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('cart/', CartDetailView.as_view(), name='cart-detail'),
    path('cart/add/', AddToCartView.as_view(), name='cart-item-create'),
    path('cart/<int:pk>/remove/', RemoveCartItemView.as_view(), name='remove-cart-item'),
    path('cart/<int:pk>/decrease/', DecreaseCartItemQuantityView.as_view(), name='decrease-cart-item-quantity'),
    path('cart/<int:pk>/increase/', IncreaseCartItemQuantityView.as_view(), name='increase-cart-item-quanity')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)