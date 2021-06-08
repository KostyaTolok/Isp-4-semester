from asgiref.sync import sync_to_async
from cart.models import Cart
from orders.models import OrderItem, Order
from users.models import UserProfile


@sync_to_async
def get_cart(user):
    return Cart.objects.get(user=user)


@sync_to_async
def update_or_create_order_item(order, item):
    return OrderItem.objects.update_or_create(
        order=order, product=item.product, quantity=item.quantity
    )


@sync_to_async
def get_user_profile(user):
    return UserProfile.objects.get(user=user)


@sync_to_async
def get_order(order_id):
    return Order.objects.get(id=order_id)