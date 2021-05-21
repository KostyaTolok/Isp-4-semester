from django.db import models
from users.models import User
from django.utils import timezone


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

    user = models.ForeignKey(User, verbose_name='Покупатель', on_delete=models.CASCADE)
    address = models.CharField(verbose_name='Адрес', max_length=255, blank=True)
    phone = models.CharField(verbose_name='Номер телефона', max_length=17, blank=True)
    first_name = models.CharField(verbose_name="Имя покупателя", max_length=40, blank=True)
    last_name = models.CharField(verbose_name="Фамилия покупателя", max_length=40, blank=True)
    created = models.DateField(verbose_name='Дата создания', auto_now=True)
    ready_time = models.DateField(verbose_name='Время готовности', default=timezone.now)
    status = models.CharField(verbose_name="Статус заказа", max_length=20, choices=STATUS_CHOICES, default='new_order')
    orderType = models.CharField(verbose_name="Тип заказа", max_length=20, choices=TYPE_CHOICES, default='delivery')
    payment = models.CharField(verbose_name="Тип оплаты", max_length=20, choices=PAYMENT_CHOICES, default='online')
    comment = models.CharField(verbose_name="Комментарий к заказу", blank=True)

    def __str__(self):
        return f"Заказ пользователя {self.user.email}"