# -*- coding: UTF-8 -*-

from flask_script import Manager
from cathome import app, db
from cathome.models import User, Image, Comment
import random

manager = Manager(app)


@manager.command
def init():
    '''
    m = hashlib.md5()
    db.drop_all()
    db.create_all()
    for i in range(100):
        username = u'user' + str(i + 1)
        password = u'qwer' + str(i + 1)
        salt = ''.join((random.sample(u'1234567890qwertyuiopasdfghjklzxcvbnmQWERYTUFVSDFWFLIL;+_',24)))
        m.update((password+salt).encode('utf-8'))
        password = m.hexdigest()
        db.session.add(User(username, password,salt,
                            'http://images.nowcoder.com/head/' + str(random.randint(0, 1000)) + 't.png'))
        for j in range(10):
            db.session.add(
                Image('http://images.nowcoder.com/head/' + str(random.randint(0, 1000)) + 'm.png', i + 1))
            for k in range(10):
                db.session.add(Comment('this is comment from me!', random.randint(1,300), random.randint(1,100)))

    db.session.commit()
    '''
    for i in range(5000):
        db.session.add(Comment('this is comment from me!', random.randint(1, 1000), random.randint(1, 100)))
    db.session.commit()


if __name__ == '__main__':
    manager.run()
