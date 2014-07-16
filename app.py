#!/usr/bin/python
#coding:utf-8

import json
import redis
import gitlab
import config
import common
from libs.sessions import SessionMiddleware, \
    RedisSessionStore
from flask import Flask, request, g, render_template, \
        redirect, url_for
from utils import Obj

app = Flask(__name__)
app.debug = config.DEBUG
app.secret_key = config.SECRET_KEY
app.config.update(
    SESSION_COOKIE_DOMAIN = config.SESSION_COOKIE_DOMAIN,
)

app.wsgi_app = SessionMiddleware(
        app.wsgi_app, \
        RedisSessionStore(
            key_template=config.SESSION_KEY_TEMPLE,\
            expire=config.SESSION_EXPIRE, \
            salt=config.SESSION_SALT, \
            pool=common.session_pool),
        cookie_name=config.SESSION_KEY, \
        cookie_age=config.COOKIE_MAX_AGE, \
        cookie_path='/', \
        cookie_expires=None, \
        cookie_secure=None, \
        cookie_httponly=False, \
        cookie_domain=config.COOKIE_DOMAIN, \
        environ_key=config.SESSION_ENVIRON_KEY)

rdb = redis.Redis(connection_pool=common.redis_pool)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    git = gitlab.Gitlab(config.GITLAB_HOST, verify_ssl=False)
    username = request.form['username']
    password = request.form['password']
    try:
        git.login(username, password)
        user = git.currentuser()
        g.session['user_id'] = user['id']
        g.session['user_name'] = user['username']
        g.session['email'] = user['email']
        g.session['is_admin'] = user['is_admin']
        groups = git.getgroups()
        g.session['groups'] = json.dumps(groups)
        rdb.hmset(config.IRC_ORGANIZATION_USERS, {user['id']: user['username']})
        key = config.IRC_USER_CHANNELS_FORMAT % user['id']
        values = dict((group['name'], group['id']) for group in groups)
        rdb.delete(key)
        rdb.hmset(key, values)
    except Exception:
        import traceback
        traceback.print_exc()
        return render_template('login.html', error=1)
    return redirect(url_for('index'))

@app.route("/")
def index():
    if not g.current_user:
        return redirect(url_for('login'))
    return render_template(
        'index.html',
        groups = g.current_user.groups,
    )

@app.before_request
def before_request():
    g.session = request.environ.get(config.SESSION_ENVIRON_KEY)
    if not g.session:
        g.current_user = None
    else:
        g.current_user = Obj()
        g.current_user.uid = g.session['user_id']
        g.current_user.uname = g.session['user_name']
        g.current_user.email = g.session['email']
        g.current_user.is_admin = g.session['is_admin']
        g.current_user.groups = json.loads(g.session['groups'])

if __name__ == "__main__":
    app.run()

