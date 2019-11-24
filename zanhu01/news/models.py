#!/usr/bin/python3
# _*_ coding:utf-8
# __author__ = 'summer'

from __future__ import unicode_literals
import uuid

from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from django.conf import settings
from zanhu01.users.models import User

class News(models.Model):
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL,
                             related_name="publisher", verbose_name="用户")
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE,
                               related_name="thread", verbose_name="自关联")
    content = models.TextField(verbose_name="动态内容")
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='linked_news', verbose_name='点赞用户')
    reply = models.BooleanField(default=False, verbose_name='是否为评论')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '首页'
        verbose_name_plural = verbose_name
        ordering = ("-created_at",)

    def __str__(self):
        return self.content

    def switch_like(self, user):
        """点赞或取消赞"""
        # 如果用户已经赞过，则取消
        if user in self.liked.all():
            self.liked.remove(user)
        # 如果没有赞过，则添加赞
        else:
            self.liked.add(user)

    def get_partent(self):
        """返回自关联中的上级记录或者本身"""
        if self.parent:
            return self.parent
        else:
            return self

    def reply_this(self, user, text):
        """
        回复首页的动态
        :param user: 登录用户
        :param text: 回复内容
        :return: None
        """
        parent = self.get_partent()
        News.objects.create(
            user=user,
            content=text,
            reply=True,
            parent=parent
        )

    def get_thread(self):
        """关联自己当前所有记录"""
        parent = self.get_partent()
        return parent.thread.all()

    def comment_count(self):
        """评论数"""
        return self.get_thread().count()

    def count_likers(self):
        """点赞数"""
        return self.liked.count()

    def get_liked(self):
        """获取点赞用户"""
        return self.liked.all()
