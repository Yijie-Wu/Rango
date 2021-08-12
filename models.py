# -*- encoding:utf-8 -*-
"""
Author: Yijie.Wu
Email: 1694517106@qq.com
Date: 2021/8/11 下午10:50
"""
from app import db
from app import Settings


class Settings(db.Model):
    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    content = db.Column(db.Text)


class GitIssues(db.Model):
    __tablename__ = "gitissues"

    id = db.Column(db.Integer, primary_key=True)
    settings = db.Column(db.Text)
    content = db.Column(db.Text)
