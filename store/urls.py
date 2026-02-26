from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='store.home'),
    path('product/<int:product_id>/', views.product, name='store.product'),
    path('category/<int:category_id>/', views.category, name='store.category'),
    path('category/', views.category, name='store.category'),
    path('cart/', views.cart, name='store.cart'),
    path('checkout/', views.checkout, name='store.checkout'),
    path('checkout/complete/', views.checkout_complete, name='store.checkout_complete'),
    path('cart/add/<int:product_id>/', views.cart_update, name='store.cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='store.cart_remove'),
    path('search/', views.search_api, name='store.search_api'),
]
