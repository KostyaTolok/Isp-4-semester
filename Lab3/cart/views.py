from django.shortcuts import render
from django.views.generic.detail import View
from users.models import User, UserProfile
from .utilities import update_cart
from .models import Cart, CartProduct
from products.models import Product
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin


class CartView(LoginRequiredMixin, View):

    def get(self, request):
        cart_obj = Cart.objects.get(user=request.user)
        return render(request, 'cart/cart_detail.html', {'cart': cart_obj})


class AddToCartView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        cart = Cart.objects.get(user=request.user)
        product = Product.objects.get(slug=kwargs.get('slug'))
        cart_product, created = CartProduct.objects.get_or_create(
            user=cart.user, cart=cart, product=product,
            overall_price=product.price
        )
        if created:
            cart.products.add(cart_product)
        else:
            cart_product.quantity += 1
            cart_product.save()
        update_cart(cart)
        return HttpResponseRedirect('/cart/')


class DeleteFromCartView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        cart = Cart.objects.get(user=request.user)
        product = Product.objects.get(slug=kwargs.get('slug'))
        cart_product = CartProduct.objects.get(
            user=cart.user, cart=cart, product=product
        )
        cart.products.remove(cart_product)
        cart_product.delete()
        update_cart(cart)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ChangeQuantityInCart(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        cart = Cart.objects.get(user=request.user)
        product = Product.objects.get(slug=kwargs.get('slug'))
        cart_product = CartProduct.objects.get(
            user=cart.user, cart=cart, product=product
        )
        quantity = int(request.POST.get('quantity'))
        cart_product.quantity = quantity
        cart_product.save()
        update_cart(cart)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
