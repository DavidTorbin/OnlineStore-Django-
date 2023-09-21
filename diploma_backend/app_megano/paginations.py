from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response


class ProductPagination(PageNumberPagination, LimitOffsetPagination,):
    default_limit = 5
    max_limit = 60
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 60

    def get_paginated_response(self, data):
        return Response({
            'items': data,
            'currentPage': self.get_page_number(self.request, data),
            'lastPage': self.page.paginator.num_pages
        })