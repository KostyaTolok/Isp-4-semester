from django.shortcuts import render
from django.views.generic.detail import View, DetailView
from .models import Product, Category


class HomeView(View):
    products = Product.objects.all()

    def get(self, request):
        return render(request, 'shop/home.html', {'products': self.products})


def index(request):
    products = Product.objects.all()
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
