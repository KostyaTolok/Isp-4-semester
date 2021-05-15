from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Product


def index(request):
    products = Product.objects.all()
    return render(request, 'shop/home.html', {'products': products})


class ProductDetailView(DetailView):
    model = Product

    template_name = 'shop/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context
