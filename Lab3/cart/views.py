from django.shortcuts import render
from django.views.generic.detail import View
from users.models import User, UserProfile
from .models import Cart


class CartView(View):

    def get(self, request):
        cart_obj = Cart.objects.get(user=request.user)
        return render(request, 'cart/cart_detail.html', {'cart': cart_obj})
