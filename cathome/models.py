# -*- coding: UTF-8 -*-

from cathome import app, db, login_manager
from datetime import datetime
from flask_login import AnonymousUserMixin


class User(db.Model):
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(12), unique=True)
    password = db.Column(db.String(128))
    images = db.relationship('Image', backref='user', lazy='dynamic')
    head_url = db.Column(db.String(128))
    salt = db.Column(db.String(24))

    def __init__(self, name, password, salt, head_url):  # , url
        self.name = name
        self.password = password
        self.head_url = head_url
        self.salt = salt

    def __repr__(self):
        return 'User:<id: %d, %s>' % (self.id, self.name)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


@login_manager.user_loader
def load_user(userid):
    return User.query.filter_by(id=userid).first()


class Image(db.Model):
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(512))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    create_date = db.Column(db.DateTime)
    comments = db.relationship('Comment')
    #show_comment_count = db.Column(db.Integer(256))
    def __init__(self, url, user_id):
        self.url = url
        self.user_id = user_id
        self.create_date = datetime.now()

    def __repr__(self):
        return 'Image from User<%d>:%s' % (self.user_id, self.url)


class Comment(db.Model):
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(1024))
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))
    from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    create_date = db.Column(db.DateTime)
    user = db.relationship('User')
    image = db.relationship('Image')
    status = db.Column(db.Integer, default=0)

    def __init__(self, content, image_id, from_user_id):
        self.content = content
        self.image_id = image_id
        self.from_user_id = from_user_id
        self.create_date = datetime.now()

    def __repr__(self):
        return 'image(%d): comment(\"%s\") is from user(%d)' % (self.image_id, self.content, self.from_user_id)
