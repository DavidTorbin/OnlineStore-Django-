from django.contrib import admin

from .models import Orders, ProductInOrder, DeliveryType, Status, PaymentType


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductInOrder)
class ProductInOrderAdmin(admin.ModelAdmin):
    pass


@admin.register(DeliveryType)
class DeliveryTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass


@admin.register(PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    pass

