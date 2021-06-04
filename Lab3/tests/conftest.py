import pytest
from django.contrib.auth import get_user_model

from cart.models import *
from users.models import User, UserProfile
from products.models import Product, Category


@pytest.fixture
def user_data(db):
    user = User.objects.create(email='test@gmail.com', login="test_user", password="test_password")
    return user


@pytest.fixture
def user_cart_data(db):
    user = User.objects.create(email='test@gmail.com', login="test_user", password="test_password")
    Cart.objects.create(user=user)

    return user


@pytest.fixture
def user_cart_product_data(db):
    user = User.objects.create(email='test@gmail.com', login="test_user", password="test_password")
    cart = Cart.objects.create(user=user)

    return user

@pytest.fixture
def user_profile_data(db):
    user = User.objects.create(email='test@gmail.com', login="test_user", password="test_password")
    user_profile = UserProfile.objects.create(user=user, address='test', first_name='test', last_name='test',
                                              phone_number='test')
    return user_profile


@pytest.fixture
def product_data(db):
    category = Category.objects.create(name='test_category', slug='test')
    product = Product.objects.create(name="test_product", slug='test', category=category, image='test',
                                     description='test', price=0)
    return product


@pytest.fixture
def category_data(db):
    category = Category.objects.create(name='test_category', slug='test')

    return category
