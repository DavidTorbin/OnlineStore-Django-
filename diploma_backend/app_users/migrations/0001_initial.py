# Generated by Django 4.1.7 on 2023-03-09 18:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=128, verbose_name='Город')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
            },
        ),
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='Название карты')),
                ('number', models.CharField(max_length=19, verbose_name='Номер карты')),
                ('name', models.CharField(blank=True, max_length=128, null=True, verbose_name='Имя владельца карты')),
                ('month', models.IntegerField(verbose_name='Месяц окончания срока действия карты')),
                ('year', models.IntegerField(verbose_name='Год окончания срока действия карты')),
                ('code', models.IntegerField(verbose_name='Секретный код с обратной стороны карты')),
            ],
            options={
                'verbose_name': 'Способ оплаты',
                'verbose_name_plural': 'Способы оплаты',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=12, verbose_name='Номер телефона')),
                ('avatar', models.ImageField(blank=True, upload_to='ava/', verbose_name='Аватарка')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Профиль пользователя',
                'verbose_name_plural': 'Профили пользователей',
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=256, verbose_name='Адрес')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app_users.cities', verbose_name='Город')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_users.userprofile')),
            ],
            options={
                'verbose_name': 'Адрес',
                'verbose_name_plural': 'Адреса',
            },
        ),
    ]
