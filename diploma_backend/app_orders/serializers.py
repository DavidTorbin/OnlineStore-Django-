from django.contrib.auth.models import User
from rest_framework import serializers
from django.db.models import Q

from app_orders.models import Orders, ProductInOrder
from app_megano.models import Products
from app_megano.serializers import ProductSerializer


class OrdersSerializer(serializers.Serializer):
    orderId = serializers.CharField(source='id')
    createdAt = serializers.DateTimeField(format='%Y-%m-%d %H:%M', input_formats=None)
    fullName = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    phone = serializers.CharField(source='user_profile.phone')
    deliveryType = serializers.CharField(source='deliveryType.name')
    paymentType = serializers.CharField(source='paymentType.name')
    status = serializers.CharField(source='status.name')
    city = serializers.CharField(source='city.city')
    address = serializers.CharField(source='address.address')
    totalCost = serializers.DecimalField(max_digits=12, decimal_places=2)
    products = serializers.SerializerMethodField()

    class Meta:
        model = Orders
        fields = ['orderId', 'createdAt', 'fullName', 'email', 'phone', 'deliveryType', 'paymentType', 'totalCost',
                  'status', 'city', 'address', 'products']

    def get_fullName(self, obj):
        return obj.user_profile.user.get_full_name()

    def get_email(self, obj):
        return obj.user_profile.user.email

    def get_products(self, obj):
        products_in_order = list()
        for i_item in ProductInOrder.objects.filter(order=obj.id):
            product = Products.objects.get(id=i_item.product.id)
            product_order = ProductInOrder.objects.get(Q(order=obj.id) & Q(product=product))
            product.count = product_order.count
            product.price = product_order.price
            products_in_order.append(product)
        return ProductSerializer(products_in_order, many=True).data


class CreateOrderSerializer(ProductSerializer):

    class Meta:
        model = Products
        fields = ['id', 'price', 'count']