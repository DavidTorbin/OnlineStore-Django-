from django.contrib import admin
from django.urls import path

from app_orders.views import OrdersViewSet


app_name = 'app_orders'


urlpatterns = [
    path('orders', OrdersViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='orders'),
    path('orders/<int:pk>', OrdersViewSet.as_view({'get': 'retrieve', 'post': 'update'}),
         name='orders'),
    path('orders/active', OrdersViewSet.as_view({'get': 'get_active_order'}),
         name='get_orders_active'),
    ]

