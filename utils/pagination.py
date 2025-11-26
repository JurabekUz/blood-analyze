from rest_framework import pagination
from rest_framework.response import Response


class CommonPagination(pagination.PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    invalid_page_message = 'An error occurred on the pagination'

    def get_paginated_response(self, data):
        self.page_size = int(self.request.query_params.get(self.page_size_query_param, self.page_size))
        totals = getattr(self, 'totals', None)

        return Response({
            'currentPage': self.page.number,
            "countItemsOnPage": len(self.page),
            'totalPages': self.page.paginator.num_pages,
            'count': self.page.paginator.count,
            'pageSize': self.page_size,
            'results': data,
            'totals': totals
        })
