from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import LimitOffsetPagination

from rest_framework.response import Response
import math
import os

class ApiPagination(PageNumberPagination):
    page_size = int(os.getenv('API_PAGINATOR_LIMIT', default=10))
    page_size_query_param = "page_size"

    def get_paginated_response(self, data):
        if self.request.query_params.get('page_size'):
            self.page_size = int(self.request.query_params.get('page_size'))

        total_page = math.ceil(self.page.paginator.count / self.page_size)
        return Response({
            'page' : {
                'count_result' : self.page.paginator.count,
                'total_page' : total_page,
                'per_page' : self.page_size,
                'current_page' : self.page.number,
            },
            'links' : {
                'previous' : self.get_previous_link(),
                'next' : self.get_next_link(),
            },
            'results' : data
        })
        

class SingleResultPagination(LimitOffsetPagination):
    default_limit = 1
    max_limit = 1