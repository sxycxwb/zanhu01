#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__summer__'

from django.test import Client
from django.urls import reverse
from test_plus.test import TestCase

from zanhu01.news.views import News


class NewsViewsTest(TestCase):

    def setUp(self):
        self.user = self.make_user("user01")
        self.other_user = self.make_user("user02")

        self.client = Client()
        self.other_client = Client()

        # 完成用户登录
        self.client.login(username="user01", password="password")
        self.other_client.login(username="user02", password="password")

        self.first_news = News.objects.create(
            user=self.user,
            content="第一条点赞"
        )

        self.second_news = News.objects.create(
            user=self.other_user,
            content="第一条点赞"
        )

        self.third_news = News.objects.create(
            user=self.other_user,
            content="第一条点赞",
            reply=True,
            parent=self.first_news
        )

    def test_news_list(self):
        """删除动态"""
        response = self.client.get(reverse("news:list"))
        assert response.status_code == 200
        assert self.first_news in response.context["news_list"]
        assert self.second_news in response.context["news_list"]
        assert self.third_news not in response.context["news_list"]
