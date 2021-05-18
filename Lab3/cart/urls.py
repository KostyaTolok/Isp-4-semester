from django.urls import path
from .views import *

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart_detail'),
    path('add-to-cart/<slug:slug>/', AddToCartView.as_view(), name='add_to_cart'),
    path('delete-from-cart/<slug:slug>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('change-quantity/<slug:slug>/', ChangeQuantityInCart.as_view(), name='change_quantity')
]
