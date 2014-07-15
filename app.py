#!/usr/bin/python
#coding:utf-8

import config
import common
from libs.sessions import SessionMiddleware, \
    RedisSessionStore
from flask import Flask, request, g, render_template
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

@app.route("/")
def index():
    return render_template('index.html')

@app.before_request
def before_request():
    g.session = request.environ.get(config.SESSION_ENVIRON_KEY)
    if not g.session:
        g.current_user = None
    else:
        g.current_user = Obj()
        g.current_user.uid = g.sessions['id']
        g.current_user.uname = g.sessions['username']
        g.current_user.email = g.sessions['email']

if __name__ == "__main__":
    app.run()

