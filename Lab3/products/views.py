from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.detail import View, DetailView
from .models import Product, Category
from cart.models import Cart, CartProduct


class HomeView(View):
    products = Product.objects.all()

    def get(self, request):
        return render(request, 'shop/home.html', {'products': self.products})


class AddToCartView(View):

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
        cart.products_amount += 1
        cart.overall_price += cart_product.product.price
        cart.save()
        return HttpResponseRedirect('/cart/')


class ProductDetailView(DetailView):
    model = Product
    queryset = Product.objects.all()
    template_name = 'shop/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context


class CategoryDetailView(DetailView):
    model = Category
    queryset = Category.objects.all()
    template_name = "shop/category_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['products'] = context['object'].product_set.all()
        return context
