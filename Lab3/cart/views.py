from django.shortcuts import render
from django.views.generic.detail import View
from .async_requests import *
import asyncio
from .utilities import update_cart
from .models import Cart, CartProduct
from products.models import Product
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
import logging

logger = logging.getLogger(__name__)


class CartView(LoginRequiredMixin, View):

    def get(self, request):
        cart_obj = asyncio.run(get_cart(request.user))
        logger.info(f"Loading cart view for user {request.user}")
        return render(request, 'cart/cart_detail.html', {'cart': cart_obj})


class AddToCartView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        cart = asyncio.run(get_cart(request.user))
        product = asyncio.run(get_product(kwargs.get('slug')))
        cart_product, created = asyncio.run(get_or_create_cart_product(cart, product))
        if created:
            cart.products.add(cart_product)
        else:
            cart_product.quantity += 1
            cart_product.save()
        update_cart(cart)
        logger.info(f"Added product {product.id} to cart for user {request.user}")
        return HttpResponseRedirect('/cart/')


class DeleteFromCartView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        cart = asyncio.run(get_cart(request.user))
        product = asyncio.run(get_product(kwargs.get('slug')))
        cart_product = asyncio.run(get_cart_product(cart, product))
        cart.products.remove(cart_product)
        cart_product.delete()
        update_cart(cart)
        logger.info(f"Deleted cart product {cart_product.id} from cart for user {request.user}")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ChangeQuantityInCart(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        cart = asyncio.run(get_cart(request.user))
        product = asyncio.run(get_product(kwargs.get('slug')))
        cart_product = asyncio.run(get_cart_product(cart, product))
        quantity = int(request.POST.get('quantity'))
        cart_product.quantity = quantity
        cart_product.save()
        update_cart(cart)
        logger.info(f"Changed quantity for cart product {cart_product.id} for user {request.user}")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
