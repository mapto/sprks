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
import controllers.incident

if __name__ == "__main__":
    app_path = '' # when run as standalone application
    static_path = '/static'
else:
    app_path = '' # when called from Apache, use WSGI
#    app_path = '/sprks' # when called from Apache, use WSGI
    static_path = '/static'

print app_path

urls = (app_path + '', controllers.home.home,
        app_path + '/', controllers.home.home,
        app_path + '/home', controllers.home.home,
        app_path + '/login', controllers.login.login,
        app_path + '/register', controllers.register.register,
        app_path + '/pwrecovery/(.*)', controllers.pwrecovery.pwrecovery,
        app_path + '/pwrecovery', controllers.pwrecovery.pwrecovery,
        app_path + '/pwrequest', controllers.pwrequest.pwrequest,
        app_path + '/password', controllers.pwrequest.pwrequest, # default password is request
        app_path + '/password/request', controllers.pwrequest.pwrequest,
        app_path + '/password/recovery', controllers.pwrecovery.pwrecovery, # restful URLs
        app_path + '/password/recovery/(.*)', controllers.pwrecovery.pwrecovery, # restful URLs
        app_path + '/intro', controllers.intro.intro,
        app_path + '/score', controllers.score.score,
        app_path + '/score/multiple', controllers.score.multiple_score,
        app_path + '/pwpolicy', controllers.pwpolicy.pwpolicy, # this URL is also being used in views/index.html for AJAX services
        app_path + '/policy', controllers.pwpolicy.pwpolicy, # default policy is password policy
        app_path + '/policy/password', controllers.pwpolicy.pwpolicy, # restful URLs
        app_path + '/forward', controllers.timeline.forward,
        app_path + '/incident', controllers.incident.incident,
        app_path + '/incident_rest', controllers.incident.incident_rest
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
