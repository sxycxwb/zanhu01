#!/usr/bin/python3
# _*_ coding:utf-8
# __author__ = 'summer'

from functools import wraps
from django.http import HttpResponseBadRequest
from django.views.generic import View
from django.core.exceptions import PermissionDenied


def ajax_required(f):
    """验证是否为AJAX请求"""

    @wraps(f)
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest("不是AJAX请求！")
        return f(request, *args, **kwargs)

    return wrap


class AuthorRequireMixin(View):
    """验证是否为原作者，用户状态删除、文章编辑"""

    def dispatch(self, request, *args, **kwargs):
        """状态实例和文章有User属性"""
        if self.get_object().user.username != self.request.user.username:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
