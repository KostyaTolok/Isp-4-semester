from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(verbose_name='Имя категории', max_length=255)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:category_detail', kwargs={'slug': self.slug})


class Product(models.Model):

    category = models.ForeignKey(Category, verbose_name="Категория товара", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Название товара", max_length=255)
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name="Изображение товара")
    description = models.TextField(verbose_name="Описание товара")
    price = models.DecimalField(verbose_name="Цена товара", max_digits=9, decimal_places=2)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'slug': self.slug, 'category': self.category.slug})
