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
    name = StringField('Username', validators=[DataRequired(), Length(1, 200)])
    email = StringField('Email Address', validators=[DataRequired(), Length(1, 200), Email()])
    submit = SubmitField()




class GitLabForm(FlaskForm):
    host = StringField('Gitlab Host', validators=[DataRequired(), Length(1, 4096), URL()])
    token = StringField('Gitlab Token', validators=[DataRequired(), Length(1, 200)])
    project_id = StringField('Project ID', validators=[DataRequired(), Length(1, 60)])
    store_path = StringField('Result Store Path', validators=[DataRequired()])
    submit = SubmitField()
