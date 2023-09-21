# Generated by Django 4.1.7 on 2023-03-16 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_megano', '0003_alter_category_subcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='active',
            field=models.BooleanField(default=False, verbose_name='Aктивные категории товаров'),
        ),
        migrations.AddField(
            model_name='products',
            name='active',
            field=models.BooleanField(default=False, verbose_name='Aктивные категории товаров'),
        ),
        migrations.AddField(
            model_name='subcategories',
            name='active',
            field=models.BooleanField(default=False, verbose_name='Aктивные подкатегории товаров'),
        ),
    ]