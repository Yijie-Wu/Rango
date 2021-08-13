import os
import sys
from flask import Flask
from pyfladesk import init_gui
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

basedir = os.path.abspath(os.path.dirname(__file__))

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class Settings():
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'anything you want')


db = SQLAlchemy()
csrf = CSRFProtect()

app = Flask(__name__)
app.config.from_object(Settings)
db.init_app(app)
csrf.init_app(app)

from routes import *

if __name__ == '__main__':
    init_gui(app, window_title="Rango")
