#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^submit/', views.list, name='list'),
    url(r'^post/(\d+)/', views.post, name='post'),
]