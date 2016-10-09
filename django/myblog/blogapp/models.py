#! /usr/bin/env python
# -*- coding:utf-8 -*-

from django.db import models

class Post(models.Model):
    post_text = models.TextField(blank=False)
    pub_date = models.DateTimeField(u'发布日期')

    class Meta:
        ordering = ['-pub_date']

    def __unicode__(self):
        return self.post_text

class Comment(models.Model):
    comment_text = models.CharField(max_length=200)
    post = models.ForeignKey(Post, default=None)

    def __unicode__(self):
        return self.comment_text