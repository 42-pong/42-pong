from rest_framework import decorators, request, response


@decorators.api_view(["GET"])
def health_check(request: request.Request) -> response.Response:
    return response.Response({"status": "OK"})
