from rest_framework import pagination


class PageNumberPagination(pagination.PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 100


class LargeResultsSetPagination(pagination.PageNumberPagination):
    page_size = 200
    page_size_query_param = "page_size"
    max_page_size = 1000
