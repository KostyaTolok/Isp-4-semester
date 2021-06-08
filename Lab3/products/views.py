from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.detail import View, DetailView
from .models import Product, Category
from cart.models import Cart, CartProduct
import asyncio
import logging

logger = logging.getLogger(__name__)


class HomeView(View):

    def get(self, request):
        products = Product.objects.all()
        logger.info("Home view loading")
        return render(request, 'shop/home.html', {'products': products})


class SearchView(View):

    def post(self, request):
        search = request.POST['search']
        logger.info(f"Searching for {search}")
        products = Product.objects.filter(name__icontains=search)
        return render(request, 'shop/home.html', {'products': products})


class ProductDetailView(DetailView):
    model = Product
    queryset = Product.objects.all()
    template_name = 'shop/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        logger.info("Product detail view loading")
        return context


class CategoryDetailView(DetailView):
    model = Category
    queryset = Category.objects.all()
    template_name = "shop/category_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['products'] = context['object'].product_set.all()
        logger.info("Category detail view loading")
        return context
