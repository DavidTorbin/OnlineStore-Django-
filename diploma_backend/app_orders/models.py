from django.db import models

from app_users.models import UserProfile, Cities, Address
from app_megano.models import Products


class DeliveryType(models.Model):
    name = models.CharField(max_length=50, null=True, blank=False, verbose_name='Тип доставки')
    description = models.TextField(null=True, blank=True, verbose_name='Описание типа доставки')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Типы доставки'
        verbose_name = 'Тип доставки'


class Status(models.Model):
    name = models.CharField(max_length=50, null=True, blank=False, verbose_name='Статус')
    description = models.TextField(null=True, blank=True, verbose_name='Описание статуса')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Статусы'
        verbose_name = 'Статус'


class PaymentType(models.Model):
    name = models.CharField(max_length=50, null=True, blank=False, verbose_name='Тип оплаты')
    description = models.TextField(null=True, blank=True, verbose_name='Описание типа оплаты')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Типы оплаты'
        verbose_name = 'Тип оплаты'


class Orders(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name='Дата оформления заказа')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления заказа')
    deliveryType = models.ForeignKey(DeliveryType, on_delete=models.PROTECT, default=2)
    paymentType = models.ForeignKey(PaymentType, on_delete=models.PROTECT, default=1)
    totalCost = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Сумма заказа')
    status = models.ForeignKey(Status, on_delete=models.PROTECT, default=1)
    city = models.ForeignKey(Cities, on_delete=models.PROTECT, default=6)
    address = models.ForeignKey(Address, on_delete=models.PROTECT, default=2)

    class Meta:
        ordering = ('-createdAt',)
        verbose_name_plural = 'Заказы'
        verbose_name = 'Заказ'

    def __str__(self):
        return 'Заказ - {}'.format(self.id)

    def get_total_cost(self):
        """
        Получение общей стоимости заказа
        :return: totalCost: Decimal
        """
        return sum(item.get_cost() for item in self.items.all())


class ProductInOrder(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Products, on_delete=models.PROTECT, related_name='order_items')
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='Стоимость единицы товара')
    count = models.PositiveSmallIntegerField(default=1, verbose_name='Количество товара в заказе')

    def get_cost(self):
        return self.price * self.count

    class Meta:
        verbose_name_plural = 'Товары в заказе'
        verbose_name = 'Товар в заказе'

    def __str__(self):
        return 'заказ № {}, наименование товара: {}'.format(self.order.id, self.product.title)
