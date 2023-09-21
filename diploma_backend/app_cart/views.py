from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import action

from app_megano.models import Products, Category
from app_cart.models import CartItems
from app_cart.CartServices import CartService
from app_cart.serializers import CartSerializer


class CartView(viewsets.ViewSet):
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated, )
    parser_classes = [JSONParser]

    def get_queryset(self):
        return (
            CartItems.objects
            .filter(user=self.request.user)
            .select_related('item_id')
        )

    def list(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_item(self, request):
        data = request.data
        int_id = int(data['id'])
        cart = CartService(request)
        cart.add_items(request, item_id=int_id, count=data['count'])
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def delete_item(self, request):
        data = request.data
        cart = CartService(request)
        cart.remove_items(request, item_id=int(data['id']), count=data['count'])
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data)

