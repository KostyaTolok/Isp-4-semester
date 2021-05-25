from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.detail import View, DetailView
from .models import Product, Category
from cart.models import Cart, CartProduct
from .filters import ProductFilter


class HomeView(View):

    def get(self, request):
        products = Product.objects.all()
        return render(request, 'shop/home.html', {'products': products})


class SearchView(View):

    def post(self, request):
        search = request.POST['search']
        products = Product.objects.filter(name__icontains=search)
        return render(request, 'shop/home.html', {'products': products})


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
