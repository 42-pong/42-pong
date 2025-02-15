from typing import Any, Mapping, Optional

from rest_framework.renderers import JSONRenderer

from .custom_response import custom_response


class ReadOnlyCustomJSONRenderer(JSONRenderer):
    """
    200, 401, 404, 500しかないようなReadOnlyなエンドポイントで使用する、カスタムレスポンスにするためのrendererクラス。
    viewsetのrender_classesにセットすることで使用できる。
    """

    def render(
        self,
        data: Optional[dict],
        accepted_media_type: Optional[str] = None,
        renderer_context: Optional[Mapping[str, Any]] = None,
    ) -> str:
        if renderer_context is None:
            return super().render(data, accepted_media_type, renderer_context)

        response = renderer_context.get("response")
        if not response:
            return super().render(data, accepted_media_type, renderer_context)

        status_code = response.status_code

        # ステータスコードによってレスポンスの形式を変更
        if status_code < 400:
            response_data = {
                custom_response.STATUS: custom_response.Status.OK,
                custom_response.DATA: data if data is not None else {},
            }
        elif status_code == 404:
            response_data = {
                custom_response.STATUS: custom_response.Status.ERROR,
                custom_response.CODE: custom_response.Code.INTERNAL_ERROR,
                custom_response.ERRORS: {"id": "The resource does not exist."},
            }
        else:
            # TODO: 401,404,500レスポンスの形式が決まれば修正
            response_data = data if data is not None else {}

        return super().render(
            response_data, accepted_media_type, renderer_context
        )
