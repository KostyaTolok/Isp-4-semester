from asgiref.sync import sync_to_async
from .models import Product, Category


@sync_to_async
def get_products():
    return Product.objects.all()


@sync_to_async
def search_products(search):
    return Product.objects.filter(name__icontains=search)


@sync_to_async
def get_categories():
    return Category.objects.all()