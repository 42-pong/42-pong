import dataclasses
from typing import Final

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import pagination, response, status

from ..custom_response import custom_response

# 1ページあたりのアイテム数のデフォルト値
DEFAULT_PAGE_SIZE: Final[int] = 20


@dataclasses.dataclass(frozen=True)
class PaginationFields:
    COUNT: str = "count"
    NEXT: str = "next"
    PREVIOUS: str = "previous"
    RESULTS: str = "results"


class CustomPagination(pagination.PageNumberPagination):
    """
    ページネーションのカスタムクラス
    複数のアイテムをlistで返す場合に使用する

    Attributes:
        page_size: 1ページあたりのアイテム数
    """

    def __init__(self, page_size: int = DEFAULT_PAGE_SIZE) -> None:
        self.page_size = page_size

    def get_paginated_response(
        self, paginated_data: list, status_code: int = status.HTTP_200_OK
    ) -> response.Response:
        """
        get_paginated_response()のオーバーライド
        ページネーションされたデータをCustomResponseに変換して返す

        Args:
            paginated_data: ページネーションされたデータ
            status_code: レスポンスのステータスコード

        Returns:
            response.Response: ページネーションされたデータがdataにセットされたCustomResponse

        Raises:
            ObjectDoesNotExist: self.pageがNoneの場合
        """
        # mypyがself.pageがNoneの可能性を検出しているため念のため例外を投げているが、恐らくNoneにはならない
        if self.page is None:
            raise ObjectDoesNotExist("CustomPagination: self.page is None.")

        data: dict = {
            PaginationFields.COUNT: self.page.paginator.count,
            PaginationFields.NEXT: self.get_next_link(),
            PaginationFields.PREVIOUS: self.get_previous_link(),
            PaginationFields.RESULTS: paginated_data,
        }
        return custom_response.CustomResponse(data=data, status=status_code)
