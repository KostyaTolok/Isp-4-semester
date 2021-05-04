from django.db import models
from products.models import Product
from users.models import User


class Cart(models.Model):

    user = models.ForeignKey(User, verbose_name="Корзина", on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, verbose_name="Продукты", blank=True, related_name="related_products")
    products_amount = models.PositiveIntegerField(verbose_name="Количество продуктов", default=0)
    overall_price = models.DecimalField(verbose_name="Цена корзины", max_digits=9, decimal_places=2)

    def __str__(self):
        return f"Корзина пользователя {self.user.email}"


class CartProduct(models.Model):

    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, verbose_name="Корзина", on_delete=models.CASCADE, related_name="related_cart")
    product = models.ForeignKey(Product, verbose_name="Продукт", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="Количество", default=1)
    overall_price = models.DecimalField(verbose_name="Цена товара", max_digits=9, decimal_places=2)

    def __str__(self):
        return f"В корзине продукт {self.product.name}"
