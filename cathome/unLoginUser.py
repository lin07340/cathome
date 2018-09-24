# -*- encoding: UTF-8 -*-

from flask_login import AnonymousUserMixin


class unLoginUser(AnonymousUserMixin):
    def __init__(self):
        self.name = 'GUEST'
        self.id = -1
