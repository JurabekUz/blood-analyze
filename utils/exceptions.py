from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_400_BAD_REQUEST


class CommonException(APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_code = HTTP_400_BAD_REQUEST
    detail = None

    def __init__(self, detail, code=None):
        super().__init__(detail, code)
        self.detail = detail
        if code is None:
            self.status_code = self.default_code