from django.contrib.auth.models import User

from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    phone = models.CharField(max_length=12, blank=True, verbose_name='Номер телефона')
    avatar = models.ImageField(upload_to='ava/', blank=True, verbose_name='Аватарка')


    class Meta:
        verbose_name_plural = 'Профили пользователей'
        verbose_name = 'Профиль пользователя'

    def __str__(self):
        return self.user.username

    def full_name(self):
        return self.user.get_full_name()


class Cities(models.Model):
    city = models.CharField(max_length=128, verbose_name='Город')

    def __str__(self):
        return self.city

    class Meta:
        verbose_name_plural = 'Города'
        verbose_name = 'Город'


class Address(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    city = models.ForeignKey(Cities, on_delete=models.PROTECT, verbose_name='Город')
    address = models.CharField(max_length=256, verbose_name='Адрес')

    def __str__(self):
        return '{}, {}'.format(self.city, self.address)

    class Meta:
        verbose_name_plural = 'Адреса'
        verbose_name = 'Адрес'


class Payments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64, verbose_name='Название карты')
    number = models.CharField(max_length=19, verbose_name='Номер карты')
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='Имя владельца карты')
    month = models.IntegerField(verbose_name='Месяц окончания срока действия карты')
    year = models.IntegerField(verbose_name='Год окончания срока действия карты')
    code = models.IntegerField(verbose_name='Секретный код с обратной стороны карты')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Способы оплаты'
        verbose_name = 'Способ оплаты'
