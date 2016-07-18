#!/usr/bin/env python
# -*- coding:utf-8 -*-  

#创建认证系统的蓝本
from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views
