from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path(r'products/<str:category>/<slug:slug>/', ProductDetailView.as_view(), name='product_detail')
]