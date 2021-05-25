from django.urls import path
from .views import *

app_name = 'orders'

urlpatterns = [
    path('make-order/', MakeOrderView.as_view(), name='make_order'),
    path('cancel-order/<int:id>/', CancelOrderView.as_view(), name='cancel_order')
]
