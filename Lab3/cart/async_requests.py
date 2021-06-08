from asgiref.sync import sync_to_async
from .models import Cart, CartProduct
from products.models import Product


@sync_to_async
def get_cart(user):
    return Cart.objects.get(user=user)


@sync_to_async
def get_product(slug):
    return Product.objects.get(slug=slug)


@sync_to_async
def get_or_create_cart_product(cart, product):
    return CartProduct.objects.get_or_create(
        user=cart.user, cart=cart, product=product
    )


@sync_to_async
def get_cart_product(cart, product):
    return CartProduct.objects.get(
        user=cart.user, cart=cart, product=product
    )
