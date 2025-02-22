from typing import Final, Optional

from django.test import TestCase
from rest_framework import request as drf_request
from rest_framework import response as drf_response
from rest_framework import status, test

from ..custom_pagination import custom_pagination
from ..custom_response import custom_response

DATA: Final[str] = custom_response.DATA

COUNT: Final[str] = custom_pagination.PaginationFields.COUNT
NEXT: Final[str] = custom_pagination.PaginationFields.NEXT
PREVIOUS: Final[str] = custom_pagination.PaginationFields.PREVIOUS
RESULTS: Final[str] = custom_pagination.PaginationFields.RESULTS


class CustomPaginationTests(TestCase):
    def setUp(self) -> None:
        # 3つのアイテムを用意(pongではmodelのインスタンスに相当)
        self.data1 = {"key1": "value1"}
        self.data2 = {"key2": "value2"}
        self.data3 = {"key3": "value3"}
        self.paginated_data = [self.data1, self.data2, self.data3]

        self.factory: test.APIRequestFactory = test.APIRequestFactory()

    def test_get_200_default_page_size(self) -> None:
        """
        デフォルト(1ページ20アイテム)のページネーションされたデータが返ることを確認
        3つのアイテムが1ページで返る
        """
        paginator: custom_pagination.CustomPagination = (
            custom_pagination.CustomPagination()  # page_sizeの指定なし(デフォルト)
        )
        request: drf_request.Request = drf_request.Request(
            self.factory.get("/")
        )

        paginated_data: Optional[list] = paginator.paginate_queryset(
            self.paginated_data,  # type: ignore[arg-type]
            request,
        )
        response: drf_response.Response = paginator.get_paginated_response(
            paginated_data  # type: ignore[arg-type]
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data[DATA],
            {
                COUNT: 3,
                NEXT: None,
                PREVIOUS: None,
                RESULTS: self.paginated_data,  # 3アイテム
            },
        )

    def test_get_200_low_page_size(self) -> None:
        """
        page sizeよりアイテム数が多い場合、複数ページに分かれて全てのアイテムが返ることを確認
        page sizeを2に設定し、1ページ目は2アイテム・2ページ目は1アイテムが返る
        """
        paginator: custom_pagination.CustomPagination = (
            custom_pagination.CustomPagination(page_size=2)  # page_sizeを指定
        )

        # 1ページ目を取得
        request: drf_request.Request = drf_request.Request(
            self.factory.get("/")
        )
        paginated_data: Optional[list] = paginator.paginate_queryset(
            self.paginated_data,  # type: ignore[arg-type]
            request,
        )
        response: drf_response.Response = paginator.get_paginated_response(
            paginated_data  # type: ignore[arg-type]
        )
        # 1ページ目のdataを確認
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data[DATA],
            {
                COUNT: 3,
                NEXT: "http://testserver/?page=2",
                PREVIOUS: None,
                RESULTS: [self.data1, self.data2],  # 2アイテム
            },
        )

        # 2ページ目を取得
        request2: drf_request.Request = drf_request.Request(
            self.factory.get("/?page=2")
        )
        paginated_data2: Optional[list] = paginator.paginate_queryset(
            self.paginated_data,  # type: ignore[arg-type]
            request2,
        )
        response2: drf_response.Response = paginator.get_paginated_response(
            paginated_data2  # type: ignore[arg-type]
        )
        # 2ページ目のdataを確認
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response2.data[DATA],
            {
                COUNT: 3,
                NEXT: None,
                PREVIOUS: "http://testserver/",
                RESULTS: [self.data3],  # 1アイテム
            },
        )

    def test_get_200_non_item(self) -> None:
        """
        アイテムが0の場合、エラーにならず空のリストが返ることを確認
        """
        paginator: custom_pagination.CustomPagination = (
            custom_pagination.CustomPagination()  # page_sizeの指定なし(デフォルト)
        )
        request: drf_request.Request = drf_request.Request(
            self.factory.get("/")
        )
        # アイテム0という意味の空リストを渡す
        paginated_data: Optional[list] = paginator.paginate_queryset(
            [],  # type: ignore[arg-type]
            request,
        )
        response: drf_response.Response = paginator.get_paginated_response(
            paginated_data  # type: ignore[arg-type]
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data[DATA],
            {
                COUNT: 0,
                NEXT: None,
                PREVIOUS: None,
                RESULTS: [],  # 0アイテム
            },
        )
