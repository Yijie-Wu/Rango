# -*- encoding:utf-8 -*-
"""
Author: Yijie.Wu
Email: 1694517106@qq.com
Date: 2021/8/11 下午11:14
"""
import os
import sys
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Text


basedir = os.path.abspath(os.path.dirname(__file__))

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data.db')

Base = declarative_base()

engine = create_engine(SQLALCHEMY_DATABASE_URI, encoding="utf-8", echo=True)


class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), unique=True)
    content = Column(Text)


class GitIssues(Base):
    __tablename__ = "gitissues"

    id = Column(Integer, primary_key=True)
    settings = Column(Text)
    content = Column(Text)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


user_info = '{"name":"your name", "email":"your email"}'

git_issues = '{"gitlab_host":"gitlab host url","token":"your gitlab token","project_id": "git project id","store_path":"choice your result store path"}'



session.add(Settings(name='user_info', content=user_info))
session.add(Settings(name='git_issues', content=git_issues))
session.commit()









