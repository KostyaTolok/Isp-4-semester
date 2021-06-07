from django.urls import path
from .views import *

app_name = 'products'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path(r'products/<slug:category>/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path(r'products/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path(r'search/', SearchView.as_view(), name='search')
]
