from django.db import models


class Category(models.Model):

    name = models.CharField(verbose_name='Имя категории', max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    category = models.ForeignKey(Category, verbose_name="Категория товара", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Название товара", max_length=255)
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name="Изображение товра")
    description = models.TextField(verbose_name="Описание товара")
    price = models.DecimalField(verbose_name="Цена товара", max_digits=9, decimal_places=2)

    def __str__(self):
        return self.name
