# -*- coding: UTF-8 -*-

from cathome import app, db
from flask import render_template, redirect, flash, get_flashed_messages, request, send_from_directory
from .models import User, Image, Comment
import re, hashlib, os
import random, json
from flask_login import login_user, logout_user, login_required, current_user
import uuid
from .qcloud import save_to_cloud


@app.route('/')
@app.route('/index/')
def index():
    images = Image.query.order_by(db.desc(Image.id)).limit(5).all()
    return render_template('index.html', images=images)


@app.route('/index/<int:page>/<int:per_page>/')
@app.route('/<int:page>/<int:per_page>/')
def index_more(page, per_page):
    paginate = Image.query.order_by(db.desc(Image.id)).paginate(page=page, per_page=per_page, error_out=False)
    map = {'has_next': paginate.has_next}
    images = []
    for image in paginate.items:
        comments = []
        show_comments = Comment.query.filter_by(image=image).filter_by(status=0).all()
        for i in range(len(show_comments), max(0, len(show_comments) - 3), -1):
            comment = show_comments[i - 1]
            comments.append(
                {'content': comment.content, 'username': comment.user.name, 'from_user_id': comment.from_user_id})
        imgvo = {'id': image.id,
                 'url': image.url,
                 'comment_count': len(show_comments),
                 'username': image.user.name,
                 'user_id': image.user_id,
                 'head_url': image.user.head_url,
                 'created_date': str(image.create_date),
                 'comments': comments,
                 'show_comments_count': min(3, len(image.comments))}
        images.append(imgvo)
    map['images'] = images
    return json.dumps(map)


@app.route('/regs/', methods={'get', 'post'})
def regs():
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()
    if username == '' or password == '':
        return redirect_with_message('/regloginpage/', u'用户名或密码不能为空', 'reglogin')
    if re.match(re.compile('^[a-zA-Z]+\w+$'), username) == None:
        return redirect_with_message('/regloginpage/', u'用户名不符合规则，请输入字母或数字，并以字母开头', 'reglogin')
    elif len(username) > 12 or len(username) < 6:
        return redirect_with_message('/regloginpage/', u'用户名长度不对，请输入6~12字符的用户名', 'reglogin')
    elif len(password) > 24 or len(password) < 8:
        return redirect_with_message('/regloginpage/', u'密码长度不对，请输入8~24字符的密码', 'reglogin')
    else:
        user = User.query.filter_by(name=username).first()
        if user != None:
            return redirect_with_message('/regloginpage/', u'用户名已存在', 'reglogin')

    # username and password is correct:
    m = hashlib.md5()
    salt = ''.join((random.sample(u'1234567890qwertyuiopasdfghjklzxcvbnmQWERYTUFVSDFWFLIL;+_', 24)))
    m.update((password + salt).encode('utf-8'))
    password = m.hexdigest()

    db.session.add(User(username, password, salt,
                        'http://images.nowcoder.com/head/' + str(random.randint(0, 1000)) + 't.png'))
    db.session.commit()
    user = User.query.filter_by(name=username).first()
    login_user(user)
    next = request.values.get('next')
    if next != None and next.startswith('/') > 0:
        return redirect(next)
    return redirect('/')


@app.route('/login/', methods={'get', 'post'})
def login():
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()
    if username == '' or password == '':
        return redirect_with_message('/regloginpage/', u'用户名或密码不能为空', 'reglogin')
    user = User.query.filter_by(name=username).first()
    if user == None:
        return redirect_with_message('/regloginpage/', u'没有此用户名', 'reglogin')

    # username is true:
    user = User.query.filter_by(name=username).first()
    salt_store = user.salt
    password_store = user.password
    m = hashlib.md5()
    m.update((password + salt_store).encode('utf-8'))
    password = m.hexdigest()
    if password != password_store:
        return redirect_with_message('/regloginpage/', u'密码错误', 'reglogin')

    login_user(user)

    next = request.values.get('next')
    if next != None and next.startswith('/') > 0:
        return redirect(next)
    return redirect('/')


@app.route('/regloginpage/', methods={'get', 'post'})
def regloginpage():
    mes = ''
    for m in get_flashed_messages(with_categories=False, category_filter=['reglogin']):
        mes += m
    return render_template('login.html', mes=mes, next=request.args.get('next'))


@app.route('/image/<int:image_id>/')
@login_required
def image(image_id):
    msg = ''
    for m in get_flashed_messages(with_categories=False, category_filter=['remove_comment']):
        msg += m
    image = Image.query.filter_by(id=image_id).first()
    comments = Comment.query.filter_by(image=image).order_by(db.desc(Comment.id)).all()
    if image == None:
        return redirect('/')
    return render_template('pageDetail.html', image=image, comments=comments, msg=msg)


@app.route('/profile/<int:user_id>/')
@login_required
def profile(user_id):
    mes = ''
    for m in get_flashed_messages(with_categories=False, category_filter=['upload']):
        mes += m
    user = User.query.filter_by(id=user_id).first()
    if user == None:
        return redirect('/')
    pagination = Image.query.filter_by(user_id=user_id).paginate(page=1, per_page=3)

    return render_template('profile.html', user=user, has_next=pagination.has_next, images=pagination.items, mes=mes)


@app.route('/profile/images/<int:user_id>/<int:page>/<int:per_page>/')
def user_images(user_id, page, per_page):
    pagination = Image.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page)

    map = {'has_next': pagination.has_next}
    images = []
    for image in pagination.items:
        comments = Comment.query.filter_by(image=image).filter_by(status=0).all()
        imgvo = {'id': image.id, 'url': image.url, 'comment_count': len(comments)}
        images.append(imgvo)
    map['images'] = images
    return json.dumps(map)


@app.route('/add_comment/', methods={'post'})
def add_comment():
    content = request.values.get('content')
    image_id = int(request.values.get('image_id'))
    if current_user.name != 'GUEST':
        print(current_user)
        comment = Comment(content, image_id, current_user.id)
        db.session.add(comment)
        db.session.commit()
        map = {'code': 0,
               'content': content,
               'user_name': current_user.name,
               'user_id': current_user.id,
               'comment_id': comment.id
               }

        return json.dumps(map)
    else:
        return json.dumps({'code': -2})

@app.route('/remove_comment/<int:comment_id>/')
def remove_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    if current_user.id == comment.image.user_id or current_user.id == comment.from_user_id:
        comment.status = 1
        print('comment remove')
        db.session.commit()
        return redirect_with_message('/image/' + str(comment.image.id) + '/', u'删除成功！', 'remove_comment')
    return redirect_with_message('/image/' + str(comment.image.id) + '/', u'您没有删除权限！', 'remove_comment')


def save_to_local(file, file_name):
    save_dir = app.config['UPLOAD_DIR']
    file.save(os.path.join(save_dir, file_name))
    return '/image/' + file_name


@app.route('/upload/', methods={'post'})
def upload():
    file = request.files['file']
    file_ext = ''
    file_name = ''
    if file.filename.find('.') > 0:
        file_ext = file.filename.rsplit('.')[1].strip().lower()
        if file_ext in app.config['ALLOW_EXT']:
            file_name = str(uuid.uuid1()).replace('-', '') + '.' + file_ext
            # url = save_to_local(file, file_name)
            url = save_to_cloud(file, file_name)
            if url != None:
                image = Image(url, current_user.id)
                db.session.add(image)
                db.session.commit()
                return redirect_with_message('/profile/' + str(current_user.id) + '/', u'保存成功', 'upload')
            else:
                return redirect_with_message('/profile/' + str(current_user.id) + '/', u'出错，请重试！', 'upload')
        else:
            return redirect_with_message('/profile/' + str(current_user.id) + '/', u'文件格式不对', 'upload')
    else:
        return redirect_with_message('/profile/' + str(current_user.id) + '/', u'文件格式不对', 'upload')


@app.route('/image/<image_name>/')
def view_image(image_name):
    return send_from_directory(app.config['UPLOAD_DIR'], image_name)


def redirect_with_message(target, message, category):
    if message != None:
        flash(message, category=category)
    return redirect(target)


@login_required
@app.route('/logout/')
def logout():
    logout_user()
    return redirect_with_message('/', u'退出登陆', 'regloginpage')
