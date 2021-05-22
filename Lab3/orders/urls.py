from django.urls import path
from .views import *

app_name = 'orders'

urlpatterns = [
    path('make-order/', MakeOrderView.as_view(), name='make_order')
]
