from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from cart.models import Cart
from .forms import OrderForm
from users.models import UserProfile
from .models import *
from cart.utilities import update_cart


class MakeOrderView(View):

    def get(self, request):
        cart_obj = Cart.objects.get(user=request.user)
        form = OrderForm(request.POST)
        return render(request, 'orders/make_order.html', {'cart': cart_obj, 'form': form})

    def post(self, request):
        form = OrderForm(request.POST)
        user = request.user
        cart = Cart.objects.get(user=request.user)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = user
            cleaned_data = form.cleaned_data
            order.address = cleaned_data.get('address')
            order.phone = cleaned_data.get('phone')
            order.first_name = cleaned_data.get('first_name')
            order.last_name = cleaned_data.get('last_name')
            order.ready_date = cleaned_data.get('ready_date')
            order.ready_time = cleaned_data.get('ready_time')
            order.status = 'new_order'
            order.payment = cleaned_data.get('payment')
            order.orderType = cleaned_data.get('orderType')
            order.comment = cleaned_data.get('comment')
            order.save()

            for item in cart.products.all():
                order_item, created = OrderItem.objects.update_or_create(
                    order=order, product=item.product, quantity=item.quantity
                )
                order_item.save()
                order.products.add(order_item)
                item.delete()
            update_cart(cart)
            user_profile = UserProfile.objects.get(user=user)
            user_profile.orders.add(order)
            user_profile.save()
            return HttpResponseRedirect('/')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class CancelOrderView(View):

    def get(self, request, *args, **kwargs):
        order = Order.objects.get(id=kwargs.get('id'))
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.orders.remove(order)
        order.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))