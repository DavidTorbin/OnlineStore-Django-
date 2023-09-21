from django.contrib import admin

from app_cart.models import CartItems


@admin.register(CartItems)
class CartItemAdmin(admin.ModelAdmin):
    pass

