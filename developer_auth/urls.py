from django.urls import path
from .views import (
    get_product_form, login, register, revoke_key, api_key,logout, generate_api_key, regenerate_api_key,index, docs, live_implementation, dashboard, support, prerequisite, authentication,
    product_create, product_delete, product_get_all, product_get_one, product_update, products_overview,
    orders_cancel, orders_create, orders_get_all, orders_get_one, orders_overview,
    cart_overview, cart_add, cart_decrease, cart_get, cart_increase, cart_remove,
    category_create, category_delete, category_get, category_overview, category_update,
    review_create, review_delete, review_get_all, review_get_one, review_overview, review_update,
    api_keys, products, order, webhooks, documetation, cheat_sheet,
    create_category, create_product, load_categories, update_product, settings, delete_account
    )

urlpatterns = [
    # Add your URL patterns here
    # Example:
    path('cheat-sheet/', cheat_sheet, name='cheat-sheet'),
    path('products/', products, name='products'),
    path('orders/', order, name='orders'),
    path('api-keys/', api_keys, name='api-keys'),
    path('webhooks/', webhooks, name='webhooks'),
    path('documentation/', documetation, name='documentation'),
    path('', index, name='index'),
    path('auth/login/', login, name='login'),
    path('auth/register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('key/', api_key, name='api-key'),
    path('api-key/', generate_api_key, name='generate-api-key'),
    path('api-key/revoke/<str:public_key>/', revoke_key, name='revoke-key'),
    path('api-key/regenerate/', regenerate_api_key, name='regenerate-key'),
    path('docs/', docs, name='docs'),
    path('docs/authentication/', authentication, name='authentication'),
    path('support/', support, name='support'),
    path('dashboard/', dashboard, name='dashboard'),
    path('docs/prerequisite/', prerequisite, name='prerequisite'),
    path('docs/implementation/', live_implementation, name='implementation'),
    path('docs/product/', products_overview, name='product-overview'),    
    path('docs/product/create/', product_create, name='product-create'),
    path('docs/product/delete/', product_delete, name='product-delete'),
    path('docs/product/get-all/', product_get_all, name='product-get-all'),
    path('docs/product/get-one/', product_get_one, name='product-get-one'),
    path('docs/product/update/', product_update, name='product-update'),

    path('docs/orders/', orders_overview, name='order-overview'),
    path('docs/orders/create/', orders_create, name='order-create'),
    path('docs/orders/get-all/', orders_get_all, name='order-get-all'),
    path('docs/orders/get-one/', orders_get_one, name='order-get-one'),
    path('docs/orders/cancel/', orders_cancel, name='order-cancel'),

    path('docs/category/', category_overview, name='category-overview'),
    path('docs/category/create/', category_create, name='category-create'),
    path('docs/category/get/', category_get, name='category-get'),
    path('docs/category/delete/', category_delete, name='category-delete'),
    path('docs/category/update/', category_update, name='category-update'),

    path('docs/review/', review_overview, name='review-overview'),
    path('docs/review/create/', review_create, name='review-create'),
    path('docs/review/update/', review_update, name='review-update'),
    path('docs/review/delete/', review_delete, name='review-delete'),
    path('docs/review/get-all/', review_get_all, name='review-get-all'),
    path('docs/review/get-one/', review_get_one, name='review-get-one'),

    path('docs/carts/', cart_overview, name='cart-overview'),
    path('docs/carts/get/', cart_get, name='cart-get'),
    path('docs/carts/increase/', cart_increase, name='cart-increase'),
    path('docs/carts/decrease/', cart_decrease, name='cart-decrease'),
    path('docs/carts/remove/', cart_remove, name='cart-remove'),
    path('docs/carts/add/', cart_add, name='cart-add'),

    path('create-category/', create_category, name='create-category'),
    path('create-product/', create_product, name='create-product'),
    path('categories/load/', load_categories, name='load-categories'),
    path('products/form/', get_product_form, name='get-product-form'),
    path('products/form/<int:pk>/', get_product_form, name='get-product-form-edit'),
    path('products/update/<str:slug>/', update_product, name='update-product'),
    path('settings/', settings, name='settings'),
    path('settings/delete/', delete_account, name='delete-account'),

]