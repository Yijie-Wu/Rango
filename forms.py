# -*- encoding:utf-8 -*-
"""
Author: Yijie.Wu
Email: 1694517106@qq.com
Date: 2021/8/11 下午10:50
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, URL, Email
from models import Settings, GitIssues


class UserForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired(), Length(1, 200)], render_kw={"class": "form-control", "placeholder": "请输入名字"})
    email = StringField('Email Address', validators=[DataRequired(), Length(1, 200), Email()], render_kw={"class": "form-control", "placeholder": "请输入邮箱地址"})
    submit = SubmitField(render_kw={"class": "btn btn-primary"})


class GitLabForm(FlaskForm):
    host = StringField('Gitlab Host', validators=[DataRequired(), Length(1, 4096), URL()], render_kw={"class": "form-control", "placeholder": "Gitlab 网址"})
    token = StringField('Gitlab Token', validators=[DataRequired(), Length(1, 200)], render_kw={"class": "form-control", "placeholder": "token"})
    project_id = StringField('Project ID', validators=[DataRequired(), Length(1, 60)], render_kw={"class": "form-control", "placeholder": "Project ID"})
    store_path = StringField('Result Store Path', validators=[DataRequired()], render_kw={"class": "form-control", "placeholder": "存放结果的地址"})
    submit = SubmitField(render_kw={"class": "btn btn-primary"})
