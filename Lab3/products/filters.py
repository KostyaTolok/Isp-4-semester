import django_filters

from models import *


class ProductFilter:

    class Meta:
        model = Product
        fields = '__all__'