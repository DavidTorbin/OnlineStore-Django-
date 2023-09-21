from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.db import models
from django.urls import reverse_lazy

product_image_path = 'images/product/'
category_image_path = 'images/category/'


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150, unique=True, null=False, blank=False, verbose_name='Название категории')
    # href = models.URLField(unique=True, null=True, blank=True, verbose_name='Ссылка')
    image_src = models.ImageField(upload_to=category_image_path, verbose_name='изображение',
                                  null=True, blank=True)
    image_alt = models.CharField(max_length=50, null=True, blank=True, verbose_name='Название')
    active = models.BooleanField(default=False, verbose_name='Aктивные категории товаров')
    index_sort = models.IntegerField(default=500, verbose_name='Индекс сортировки')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        catalog_id = str(self.id)
        return reverse_lazy('frontend:catalog_pk', kwargs={'pk': catalog_id})

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'
        ordering = ['index_sort']


class Subcategories(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 verbose_name='Категория товара',
                                 related_name='subcategories')
    title = models.CharField(max_length=150, unique=True, blank=False, verbose_name='Название подкатегории')
    # href = models.URLField(unique=True, null=False, blank=False, verbose_name='Ссылка')
    image_src = models.ImageField(upload_to=category_image_path,
                                  verbose_name='изображение',
                                  null=True, blank=True)
    image_alt = models.CharField(max_length=50, null=True, blank=True, verbose_name='Название')
    active = models.BooleanField(default=False, verbose_name='Aктивные подкатегории товаров')
    index_sort = models.IntegerField(default=500, verbose_name='Индекс сортировки')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        subcatalog_id = ''.join([str(self.category.id), str(self.id)])
        return reverse_lazy('frontend:catalog_pk', kwargs={'pk': subcatalog_id})

    class Meta:
        verbose_name_plural = 'Подкатегории'
        verbose_name = 'Подкатегория'
        ordering = ['index_sort']


class Specifications(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True, verbose_name='Характеристика')
    value = models.TextField(verbose_name='Значение характеристики')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Спецификации'
        verbose_name = 'Спецификация'


class Products(models.Model):
    category = models.ManyToManyField(Category, related_name='products')
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='Стоимость единицы товара')
    count = models.PositiveSmallIntegerField(default=0, verbose_name='Количество товара')
    title = models.CharField(max_length=150, unique=True, null=False, blank=False, verbose_name='Название товара')
    description = models.TextField(null=True, blank=True, verbose_name='Краткое описание товара')
    fullDescription = models.TextField(null=True, blank=True, verbose_name='Полное описание товара')
    freeDelivery = models.BooleanField(default=False, verbose_name='Бесплатная доставка есть/нет')
    href = models.CharField(max_length=650, unique=True, null=True, blank=True, verbose_name='Ссылка на страницу товара')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оформления товара')
    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления товара')
    tags = TaggableManager(blank=True)
    specification = models.ForeignKey(Specifications, on_delete=models.SET_NULL, null=True,
                                      verbose_name='Особенности товара')
    active = models.BooleanField(default=False, verbose_name='Aктивные категории товаров')
    limited = models.BooleanField(default=False, verbose_name='Ограниченная серия')
    banner = models.BooleanField(default=False, verbose_name='Отобразить на банере')
    rate = models.IntegerField(verbose_name='Рейтинг товара')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Товары'
        verbose_name = 'Товар'


class ProductImages(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    name = models.CharField(max_length=80, null=True, blank=True, verbose_name='Название изображения')
    imageURL = models.ImageField(upload_to=product_image_path, verbose_name='Ссылка на изображение')

    class Meta:
        verbose_name_plural = 'Изображения товара'
        verbose_name = 'Изображение товара'

    def __str__(self):
        return '{}_{}'.format(self.product, self.name)


class Reviews(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    author = models.CharField(max_length=100, null=False, blank=False, verbose_name='Автор')
    email = models.EmailField(max_length=70, blank=True, null=True)
    text = models.TextField(verbose_name='Текст отзыва')
    rate = models.IntegerField(verbose_name='Рейтинг отзыва')
    date = models.DateTimeField(verbose_name='Дата добавления отзыва')
    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения отзыва')

    class Meta:
        verbose_name_plural = 'Отзывы'
        verbose_name = 'Отзыв'

    def __str__(self):
        return '{} {}'.format(self.id, self.product)

