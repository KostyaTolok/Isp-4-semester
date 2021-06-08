from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.detail import View, DetailView
from .models import Product, Category
from cart.models import Cart, CartProduct
import asyncio
from .async_requests import *
import logging

logger = logging.getLogger(__name__)


class HomeView(View):

    def get(self, request):
        products = asyncio.run(get_products())
        logger.info("Home view loading")
        return render(request, 'shop/home.html', {'products': products})


class SearchView(View):

    def post(self, request):
        search = request.POST['search']
        logger.info(f"Searching for {search}")
        products = asyncio.run(search_products(search))
        return render(request, 'shop/home.html', {'products': products})


class ProductDetailView(DetailView):
    model = Product
    queryset = asyncio.run(get_products())
    template_name = 'shop/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        logger.info("Product detail view loading")
        return context


class CategoryDetailView(DetailView):
    model = Category
    queryset = asyncio.run(get_categories())
    template_name = "shop/category_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['products'] = context['object'].product_set.all()
        logger.info("Category detail view loading")
        return context
