from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomResponseMixin:
    """Consistent API response format:

    {
        "status": "success" | "error",
        "message": "...",
        "data": [...],          # optional
        "pagination": {...},    # optional, when paginate=True
    }
    """

    @staticmethod
    def _paginate_data(data, request, view, page_size: int = 10):
        """Paginate the given queryset/list."""
        paginator = PageNumberPagination()
        paginator.page_size = page_size
        paginated_data = paginator.paginate_queryset(data, request, view=view)

        pagination_details = {
            "count": paginator.page.paginator.count,
            "next": paginator.get_next_link(),
            "previous": paginator.get_previous_link(),
        }
        return paginated_data, pagination_details

    @staticmethod
    def success(
        message: str,
        data=None,
        paginate: bool = False,
        request=None,
        view=None,
        page_size: int = 10,
        status_code: int = status.HTTP_200_OK,
    ) -> Response:
        """Build a success response; supports optional pagination.

        When paginate=True, `request` and `view` are required.
        """
        response = {
            "status": "success",
            "message": message,
        }

        if paginate and data is not None:
            if request is None or view is None:
                raise ValueError("Pagination requires `request` and `view`.")

            paginated_data, pagination_details = CustomResponseMixin._paginate_data(data, request, view, page_size)
            response["pagination"] = pagination_details
            response["data"] = paginated_data
        elif data is not None:
            response["data"] = data

        return Response(response, status=status_code)

    @staticmethod
    def error(
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ) -> Response:
        """Build an error response."""
        response = {
            "status": "error",
            "message": message,
        }

        return Response(data=response, status=status_code)
