#!/usr/bin/env python

import sys
import os

# change current directory to the project path
# so local modules can be found even if not previously in localsys path
abspath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(abspath)
os.chdir(abspath)

import web
from localsys import storage
import controllers.home
import controllers.user
import controllers.intro
import controllers.pwpolicy
import controllers.score
import controllers.timeline
import controllers.chronos
import controllers.policy_history
import controllers.incident

urls = ('/', controllers.pwpolicy.pwpolicy,
        '/home', controllers.home.home,
        '/login', controllers.user.login,
        '/register', controllers.user.register,
        '/password', controllers.user.password,
        '/intro', controllers.intro.intro,
        '/score', controllers.score.score,
        '/score/multiple', controllers.score.multiple_score,
        '/pwpolicy', controllers.pwpolicy.pwpolicy, # this URL is also being used in views/skeleton.html for AJAX services
        '/policy', controllers.pwpolicy.pwpolicy, # default policy is password policy
        '/policy/password', controllers.pwpolicy.pwpolicy, # restful URLs
        '/forward', controllers.timeline.forward,
        '/timeline', controllers.timeline.go,
        '/history', controllers.policy_history.history,
        # APIs
        '/api/user/register', controllers.user.register,
        '/api/user/login', controllers.user.login,
        '/api/user/password(/?)(.+)', controllers.user.password,
        '/incident', controllers.incident.incident        
)

app = web.application(urls, globals(), autoreload=False)
if web.config.get('_session') is None:
    store = web.session.DBStore(storage.db, 'sessions')
    storage.session = web.session.Session(app, store, initializer={'user_id': 0})
    web.config._session = storage.session
else:
    storage.session = web.config._session

if __name__ == "__main__":
    app.run() # when run as standalone application run own server
else:
    application = app.wsgifunc() # when called from Apache, use WSGI
