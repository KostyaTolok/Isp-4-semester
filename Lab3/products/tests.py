from django.test import TestCase
from django.urls import reverse
from users.models import User
import pytest


# @pytest.mark.django_db
# def test_home_view(client):
#     url = reverse('home')
#     response = client.get(url)
#     assert response.status_code == 200


@pytest.mark.django_db
def test_user_create():
    User.objects.create(login='kostya', email='kostya@gmail.com', password='password')
    assert User.objects.count() == 1


