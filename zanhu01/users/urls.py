#!/usr/bin/python3
# _*_ coding:utf-8
# __author__ = 'summer'

from django.urls import path

from zanhu01.users import views


app_name = "users"
urlpatterns = [
    path("update", view=views.UserUpdateView.as_view(), name="update"),
    path("<str:username>/", view=views.UserDetailView.as_view(), name="detail"),
]
