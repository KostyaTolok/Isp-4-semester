from django.db import models


def update_cart(cart):
        cart_data = cart.products.aggregate(models.Sum('overall_price'), models.Sum('quantity'))
        if cart_data.get('overall_price__sum'):
            cart.overall_price = cart_data['overall_price__sum']
        else:
            cart.overall_price = 0
        if cart_data.get('quantity__sum'):
            cart.products_amount = cart_data['quantity__sum']
        else:
            cart.products_amount = 0
        cart.save()