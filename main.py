#!/usr/bin/env python

import sys
import os

# change current directory to the project path
# so local modules can be found even if not previously in system path
abspath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(abspath)
os.chdir(abspath)

import web
import session
import controllers.home
import controllers.register
import controllers.login
import controllers.intro
import controllers.pwrecovery
import controllers.pwrequest
import controllers.pwpolicy
import controllers.score
import controllers.timeline
import controllers.chronos
import controllers.policy_history

urls = ('/', controllers.pwpolicy.pwpolicy,
        '/home', controllers.home.home,
        '/login', controllers.login.login,
        '/register', controllers.register.register,
        '/pwrecovery/(.*)', controllers.pwrecovery.pwrecovery,
        '/pwrecovery', controllers.pwrecovery.pwrecovery,
        '/pwrequest', controllers.pwrequest.pwrequest,
        '/password', controllers.pwrequest.pwrequest, # default password is request
        '/password/request', controllers.pwrequest.pwrequest,
        '/password/recovery', controllers.pwrecovery.pwrecovery, # restful URLs
        '/password/recovery/(.*)', controllers.pwrecovery.pwrecovery, # restful URLs
        '/intro', controllers.intro.intro,
        '/score', controllers.score.score,
        '/score/multiple', controllers.score.multiple_score,
        '/pwpolicy', controllers.pwpolicy.pwpolicy, # this URL is also being used in views/index.html for AJAX services
        '/policy', controllers.pwpolicy.pwpolicy, # default policy is password policy
        '/policy/password', controllers.pwpolicy.pwpolicy, # restful URLs
        '/forward', controllers.timeline.forward,
        '/timeline', controllers.timeline.preview,
        '/history', controllers.policy_history.history
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
