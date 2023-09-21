from django.shortcuts import render
from django.http import Http404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import action
from decimal import Decimal

from app_orders.serializers import OrdersSerializer, CreateOrderSerializer
from app_orders.models import Orders, ProductInOrder, Status, PaymentType, DeliveryType
from app_users.models import UserProfile, Cities, Address
from app_megano.models import Products



class OrdersViewSet(viewsets.ViewSet):
    serializer_class = OrdersSerializer
    permission_classes = (IsAuthenticated, )
    parser_classes = [JSONParser]

    def get_queryset(self):
        return (
            Orders.objects
            .select_related()
            .prefetch_related()
            .filter(user_profile__user=self.request.user)
            .order_by('-createdAt')
        )

    def get_order_or_404(self):
        try:
            order = self.get_queryset().get(id=self.kwargs['pk'])
        except Orders.DoesNotExist:
            raise Http404("Заказа с данным номером не существует.")
        return order

    def list(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        profile = UserProfile.objects.get(user=request.user)
        new_order = Orders.objects.create(user_profile=profile)
        for i_item in data:
            product = Products.objects.get(id=int(i_item['id']))
            item = ProductInOrder.objects.create(
                    order=new_order,
                    product=product,
                    price=i_item['price'],
                    count=i_item['count']
            )
            item.save()
        new_order.totalCost = new_order.get_total_cost()
        new_order.save()
        queryset = self.get_queryset().first()
        serializer = self.serializer_class(queryset)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        order = self.get_order_or_404()
        serializer = self.serializer_class(order, many=False)

        return Response(serializer.data)

    def update(self, request, pk=None):
        order = self.get_order_or_404()
        items_in_order = ProductInOrder.objects.filter(order=order)
        data = request.data

        order.deliveryType = DeliveryType.objects.get(name=data['deliveryType'])
        order.paymentType = PaymentType.objects.get(name=data['paymentType'])
        order.totalCost = Decimal(data['totalCost'])
        order.status = Status.objects.get(name=data['status'])
        order.city = Cities.objects.get(city=data['city'])
        order.address = Address.objects.get(address=data['address'])
        order.save()

        for i_item in data['products']:
            item = items_in_order.filter(product=int(i_item['id']))
            if item.exists():
                item = item.get()
                item.price = i_item['price']
                item.count = i_item['count']
            else:
                item = ProductInOrder.objects.create(
                        order=order,
                        product=product,
                        price=i_item['price'],
                        count=i_item['count']
                )
            item.save()

        order = self.get_queryset().get(id=self.kwargs['pk'])
        serializer = self.serializer_class(order, many=False, partial=True)
        return Response(serializer.data)

    @action(detail=False)
    def get_active_order(self, request):
        order = self.get_queryset().first()
        serializer = self.serializer_class(order, many=False)
        return Response(serializer.data)
