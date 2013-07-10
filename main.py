#!/usr/bin/env python

import sys
import os

# change current directory to the project path
# so local modules can be found even if not previously in localsys path
abspath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(abspath)
os.chdir(abspath)

from localsys import storage

# If standalone server used (typically for development), do not change names
# because it cannot handle custom static paths.
# This needs to be done before the environment module is loaded.
# There is no obvious dependency on environment here, but in experiments this has shown to be the difference.
if __name__ == "__main__":
    storage.path = ''

import web
import controllers.home
import controllers.user
import controllers.intro
import controllers.pwpolicy
import controllers.score
import controllers.chronos
import controllers.policy_history
import controllers.incident

urls = (
        storage.path + '', controllers.pwpolicy.pwpolicy, # without the first slash still should load the page
        storage.path + '/', controllers.pwpolicy.pwpolicy,
        storage.path + '/home', controllers.home.home,
        storage.path + '/login', controllers.user.account,
        storage.path + '/register', controllers.user.register,
        storage.path + '/password', controllers.user.password,
        storage.path + '/intro', controllers.intro.intro,
        storage.path + '/score', controllers.score.score,
        storage.path + '/score/multiple', controllers.score.multiple_score,
        storage.path + '/pwpolicy', controllers.pwpolicy.pwpolicy, # this URL is also being used in views/skeleton.html for AJAX services
        storage.path + '/policy', controllers.pwpolicy.pwpolicy, # default policy is password policy
        storage.path + '/policy/password', controllers.pwpolicy.pwpolicy, # restful URLs
        storage.path + '/history', controllers.policy_history.history,
        storage.path + '/incident', controllers.incident.incident,

        # APIs
        storage.path + '/api/user/account(/?)(.+)', controllers.user.account,
        storage.path + '/api/user/account', controllers.user.account,
        storage.path + '/api/user/password(/?)(.+)', controllers.user.password,
        storage.path + '/api/chronos/sync', controllers.chronos.chronos,

        #REST
        storage.path + '/score_rest', controllers.score.score_rest,
        storage.path + '/incident_rest', controllers.incident.incident_rest,
        storage.path + '/history_rest', controllers.policy_history.history_rest,
        storage.path + '/pwpolicy_rest', controllers.pwpolicy.pwpolicy_rest
)

app = web.application(urls, globals(), autoreload=False)
if web.config.get('_session') is None:
    store = web.session.DBStore(storage.db, 'sessions')
    storage.session = web.session.Session(app, store, initializer={'user_id': 0})
    web.config._session = storage.session
else:
    storage.session = web.config._session

if __name__ == "__main__":
    app.run()  # when run as standalone application run own server
else:
    application = app.wsgifunc() # when called from Apache, use WSGI
