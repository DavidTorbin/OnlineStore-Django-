from typing import Any, List

from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers

from app_megano.views import (CategoriesViewSet, TagsViewSet, CatalogViewSet, CatalogByCategoryViewSet,
                              LimitedItemsViewSet, PopularItemsViewSet, BannerItemsViewSet, ProductItemViewSet,
                              ReviewViewSet)


app_name = 'app_megano'


urlpatterns = [
    path('categories', CategoriesViewSet.as_view({'get': 'list'}),
         name='get_categories'),
    path('tags', TagsViewSet.as_view({'get': 'list'}),
         name='get_tags'),
    path('catalog', CatalogViewSet.as_view({'get': 'list'}),
         name='get_catalog'),
    path('catalog/<int:pk>', CatalogByCategoryViewSet.as_view({'get': 'list'}),
         name='get_catalog__id_'),
    path('products/popular', PopularItemsViewSet.as_view({'get': 'list'}),
         name='get_products_popular'),
    path('products/limited', LimitedItemsViewSet.as_view({'get': 'list'}),
         name='get_products_limited'),
    path('banners', BannerItemsViewSet.as_view({'get': 'list'}),
         name='get_banners'),
    path('product/<int:pk>', ProductItemViewSet.as_view({'get': 'retrieve'}),
         name='get_product__id_'),
    path('product/<int:pk>/review', ReviewViewSet.as_view({'post': 'create'}),
         name='post_product__id__review'),
]
