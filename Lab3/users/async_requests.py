from asgiref.sync import sync_to_async
from .models import UserProfile
from cart.models import Cart


@sync_to_async
def create_cart(user):
    Cart.objects.create(user=user)


@sync_to_async
def create_user_profile(user, address, first_name, last_name, phone_number):
    UserProfile.objects.create(user=user, address=address,
                               first_name=first_name,
                               last_name=last_name,
                               phone_number=phone_number)


@sync_to_async
def get_user_profile(user):
    return UserProfile.objects.get(user=user)