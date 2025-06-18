from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # Home and product listing
    path('', views.home, name='home'),
    path('team/', views.team, name='team'),
    path('products/', views.product_list, name='product_list'),
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('trending/', views.trending_products, name='trending_products'),
    
    # Cart management
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/update/<int:product_id>/', views.cart_update, name='cart_update'),
    
    # Checkout and orders
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_list, name='order_list'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),
    path('order/<int:order_id>/mark-delivered/', views.mark_order_delivered, name='mark_order_delivered'),
    
    # Search
    path('search/', views.search, name='search'),
    
    # User profile
    path('profile/', views.profile, name='profile'),
    path('profile/orders/', views.user_orders, name='user_orders'),
    path('profile/address/', views.user_address, name='user_address'),
    path('profile/settings/', views.account_settings, name='account_settings'),
] 