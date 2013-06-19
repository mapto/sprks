#!/usr/bin/env python

import sys
import os

# change current directory to the project path
# so local modules can be found even if not previously in system path
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)

import web
import session

import controllers.register
import controllers.login
import controllers.intro
import controllers.pwrecovery
import controllers.pwrequest
import controllers.pwpolicy
import controllers.score
import controllers.timeline

urls = ('/', controllers.login.login,
        '/login', controllers.login.login,
        '/register', controllers.register.register,
        '/pwrecovery/(.*)', controllers.pwrecovery.pwrecovery,
        '/pwrecovery', controllers.pwrecovery.pwrecovery,
        '/pwrequest', controllers.pwrequest.pwrequest,
        '/intro', controllers.intro.intro,
        '/score', controllers.score.score,
        '/pwpolicy', controllers.pwpolicy.pwpolicy, # this URL is also being used in views/index.html for AJAX services
        '/policy', controllers.pwpolicy.pwpolicy,
        '/policy/password', controllers.pwpolicy.pwpolicy,
        '/forward', controllers.timeline.forward
)

app = web.application(urls, globals(), autoreload=False)
if web.config.get('_session') is None:
    session.mysession.session = web.session.Session(app, session.mysession.store, initializer={'user': 'anonymous', 'loggedin': False, 'id': 0})
    web.config._session = session
else:
    session.mysession.session = web.config._session

if __name__ == "__main__":
    app.run() # when run as standalone application run own server
else:
    application = app.wsgifunc() # when called from Apache, use WSGI
