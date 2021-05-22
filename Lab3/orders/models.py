from django.db import models
from django.utils import timezone
from products.models import Product


class Order(models.Model):

    STATUS_CHOICES = (
        ('new_order', 'Новый заказ'),
        ('order_in_process', 'Заказ в обработке'),
        ('order_ready', 'Заказ готов'),
        ('order_done', 'Заказ выполнен')
    )

    TYPE_CHOICES = (
        ('delivery', 'Доставка'),
        ('pickup', 'Самовывоз')
    )

    PAYMENT_CHOICES = (
        ('online', 'Онлайн оплата'),
        ('cash', 'Оплата наличными')
    )

    user = models.ForeignKey('users.User', verbose_name='Покупатель', on_delete=models.CASCADE, related_name='related_orders', blank=True)
    address = models.CharField(verbose_name='Адрес', max_length=255, blank=True)
    phone = models.CharField(verbose_name='Номер телефона', max_length=17, blank=True)
    first_name = models.CharField(verbose_name="Имя покупателя", max_length=40, blank=True)
    last_name = models.CharField(verbose_name="Фамилия покупателя", max_length=40, blank=True)
    created = models.DateField(verbose_name='Дата создания', auto_now=True)
    ready_date = models.DateField(verbose_name='Дата готовности', default=timezone.now)
    ready_time = models.TimeField(verbose_name='Время готовности', default=timezone.now)
    status = models.CharField(verbose_name="Статус заказа", max_length=20, choices=STATUS_CHOICES, default='new_order')
    orderType = models.CharField(verbose_name="Тип заказа", max_length=20, choices=TYPE_CHOICES, default='delivery')
    payment = models.CharField(verbose_name="Тип оплаты", max_length=20, choices=PAYMENT_CHOICES, default='online')
    comment = models.CharField(verbose_name="Комментарий к заказу", max_length=255, blank=True)
    products = models.ManyToManyField('OrderItem', verbose_name="Продукты", blank=True,
                                      related_name="related_products")

    def __str__(self):
        return f"Заказ пользователя {self.user.email}"


class OrderItem(models.Model):

    order = models.ForeignKey(Order, verbose_name='Заказ', on_delete=models.CASCADE, related_name='related_order')
    product = models.ForeignKey(Product, verbose_name="Продукт", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="Количество", default=1)
    overall_price = models.DecimalField(verbose_name="Цена товара", max_digits=9, decimal_places=2)

    def save(self, *args, **kwargs):
        self.overall_price = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Пункт заказа пользователя {self.order.user.email}"