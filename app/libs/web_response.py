from flask import jsonify
from typing import TypeVar, Generic

T = TypeVar('T')


class ErrorResponseData:
    def __init__(self, code=10001, msg='error', domain: Generic[T] = None):
        self.code = code
        self.msg = msg
        self.domain = domain

    def to_dict(self):
        return {
            'code': self.code,
            'msg': self.msg,
            'domain': self.domain
        }


class WebResponse:
    def __init__(self, data: Generic[T] = None, error: ErrorResponseData = None):
        self.data = data
        self.error = error

    @staticmethod
    def build_data(data):
        resp = WebResponse(data=data)
        return resp.to_json()

    @staticmethod
    def build_custom_error(error: ErrorResponseData):
        resp = WebResponse(error=error)
        return resp.to_json()

    @staticmethod
    def build_error(code: int, msg: str, domain: Generic[T] = None):
        error = ErrorResponseData(code, msg, domain)
        resp = WebResponse(error=error)
        return resp.to_json()

    def to_json(self):
        error = None
        if self.error:
            error = self.error.to_dict()
        return jsonify({
            'error': error,
            'data': self.data
        })
