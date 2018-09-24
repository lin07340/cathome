# -*- coding: UTF-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .unLoginUser import unLoginUser

app = Flask(__name__)
app.config.from_pyfile('app.conf')
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.secret_key = 'linpeilin'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = '/regloginpage/'
login_manager.login_message = u'请先登录！'
login_manager.login_message_category = "reglogin"

login_manager.anonymous_user = unLoginUser
from cathome import views, models
