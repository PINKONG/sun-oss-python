# -*- coding: utf-8 -*-


import functools

class SunOssError(Exception):
    def __init__(self, status, body, message):
        #: HTTP 状态码
        self.status = status

        #: HTTP响应体（部分）
        self.body = body

        #: OSS错误信息
        self.message = message

    def __str__(self):
        error = {'status': self.status,
                 'message': self.message}
        return str(error)

    def _str_with_body(self):
        error = {'status': self.status,
                 'message': self.message}
        return str(error)



"""
"""
class QiniuError(SunOssError):
    pass


class QiniuPartialSuccess(QiniuError):
    status = 298
    code = '部分操作执行成功'


class QiniuMessageFormatIllegal(QiniuError):
    status = 400
    code = '请求报文格式错误'


class QiniuAuthFaild(QiniuError):
    status = 401
    code = '认证授权失败'


class QiniuPermissionDenied(QiniuError):
    status = 403
    error = '权限不足'


class QiniuNotFound(QiniuError):
    status = 404
    error = '资源不存在'


# class InvalidRequest(QiniuError):
#     status = 405
#     error = '请求方式错误'
#
#
# class InvalidRequest(QiniuError):
#     status = 406
#     error = '上传的数据 CRC32 校验错误'
#
#
# class InvalidRequest(QiniuError):
#     status = 413
#     error = '请求资源大小大于指定的最大值'
#
#
# class InvalidRequest(QiniuError):
#     status = 419
#     error = '用户账号被冻结'
#
#
# class InvalidRequest(QiniuError):
#     status = 478
#     error = '镜像回源失败'
#
#
# class InvalidRequest(QiniuError):
#     status = 502
#     error = '错误网关'
#
#
# class InvalidRequest(QiniuError):
#     status = 503
#     error = '服务端不可用'
#
#
# class InvalidRequest(QiniuError):
#     status = 504
#     error = '服务端操作超时'
#
#
# class InvalidRequest(QiniuError):
#     status = 573
#     error = '单个资源访问频率过高'
#
#
# class InvalidRequest(QiniuError):
#     status = 579
#     error = '上传成功但是回调失败'
#
#
# class InvalidRequest(QiniuError):
#     status = 599
#     error = '服务端操作失败'
#
#
# class InvalidRequest(QiniuError):
#     status = 608
#     error = '资源内容被修改'
#
#
class QiniuObjectNotExist(QiniuError):
    status = 612
    error = '指定资源不存在或已被删除'


# class InvalidRequest(QiniuError):
#     status = 614
#     code = '目标资源已存在'


class QiniuMarkerParamIllegal(QiniuError):
    status = 630
    code = '调用列举资源(list)接口时，指定非法的marker参数'


class QiniuBreakpointTransmissionFaild(QiniuError):
    status = 701
    code = '在断点续上传过程中，后续上传接收地址不正确或ctx信息已过期'


_QINIU_ERROR_TO_EXCEPTION = {}


def qiniu_error_handler(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        ret, info = func(*args, **kwargs)

        if info.status_code != 200:
            raise _make_qiniu_exception(info)
        return ret, info
    return decorator


def _make_qiniu_exception(resp):
    code = resp.status_code
    body = resp.text_body
    message = resp.error

    try:
        klass = _QINIU_ERROR_TO_EXCEPTION[code]
        return klass(code, body, message)
    except KeyError:
        return QiniuError(code, body, message)


def _walk_subclasses(klass):
    for sub in klass.__subclasses__():
        yield sub
        for subsub in _walk_subclasses(sub):
            yield subsub


for klass in _walk_subclasses(QiniuError):
    status = getattr(klass, 'status', None)

    if status is not None:
        _QINIU_ERROR_TO_EXCEPTION[status] = klass


