#! /usr/bin/env python
# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.utils import timezone
from .models import Post


def index(request):
    return render(request, 'index.html')

def list(request):
    if request.method == 'POST':
        _post_text = request.POST['post_data']
        _pub_date = timezone.now()
        new_list = Post(post_text=_post_text, pub_date=_pub_date)
        new_list.save()
    else:
        request.POST['post_data'] = ''
    post = Post.objects.all()
    return render(request, 'index.html', {'post_list': post})

def post(request, post_id):
    if request.method == 'GET':
        _post = Post.objects.get(id=post_id)
    return render(request, 'post.html', {'post': _post})