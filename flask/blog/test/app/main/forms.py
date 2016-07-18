#!/usr/bin/env python
# -*- coding:utf-8 -*-  

from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from flask.ext.pagedown.fields import PageDownField
from ..models import Role, User


class NameForm(Form):
    name = StringField('你叫什么名字?', validators=[Required()])
    submit = SubmitField('提交')

	
class EditProfileForm(Form):
    name = StringField('真实姓名', validators=[Length(0, 64)])
    gender = SelectField('性别', choices=[('女','女'), ('男', '男'), ('保密', '保密')], validators=[Required()], coerce=str)
    location = StringField('地址', validators=[Length(0, 64)])
    about_me = TextAreaField('关于我')
    submit = SubmitField('提交')
	

class EditProfileAdminForm(Form):
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField('昵称', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    confirmed = BooleanField('已验证')
    role = SelectField('角色', coerce=int)
    gender = SelectField('性别', choices=[('女','女'), ('男', '男'), ('保密', '保密')], validators=[Required()], coerce=str)
    name = StringField('真实姓名', validators=[Length(0, 64)])
    location = StringField('地址', validators=[Length(0, 64)])
    about_me = TextAreaField('关于我')
    submit = SubmitField('提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

			
class PostForm(Form):
    body = PageDownField("想写点啥呢？", validators=[Required()])
    submit = SubmitField('发布')

	
class CommentForm(Form):
    body = StringField('想说些什么？', validators=[Required()])
    submit = SubmitField('评论')