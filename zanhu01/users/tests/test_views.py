#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__summer__'

from django.test import RequestFactory
from test_plus.test import TestCase

from zanhu01.users.views import UserUpdateView


class BaseUserTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = self.make_user()


class TestUserUpdateView(BaseUserTestCase):

    def setUp(self):
        super().setUp()
        self.view = UserUpdateView()
        """用户给视图发送了request请求，它和直接使用浏览器的区别在于不需要经过django中间件，路由，wsgi"""
        request = self.factory.get('/fake-url')
        request.user = self.user
        self.view.request = request

    def test_get_success_url(self):
        self.assertEqual(self.view.get_success_url(), '/users/testuser/')

    def test_get_object(self):
        self.assertEqual(self.view.get_object(), self.user)
