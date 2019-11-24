#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Jack__'

from django.urls import path

from zanhu01.news import views

app_name = 'news'

urlpatterns = [
    path('', views.NewsListView.as_view(), name='list'),
    path('post-news/', views.post_new, name='post-news'),
    path('delete/<str:pk>/', views.NewsDeleteView.as_view(), name='delete_news')
]
