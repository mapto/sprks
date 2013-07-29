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
import controllers.score
import controllers.chronos
import controllers.policy_history
import controllers.incident
import controllers.pwpolicy
import controllers.spa
import controllers.user_spa
import controllers.characters

urls = (
        storage.path + '', controllers.spa.spa,
        storage.path + '/', controllers.spa.spa,
        storage.path + '/score', controllers.score.score,
        storage.path + '/score/multiple', controllers.score.multiple_score,
        storage.path + '/history', controllers.policy_history.history,
        storage.path + '/incident', controllers.incident.incident,
        storage.path + '/policy/password', controllers.pwpolicy.pwpolicy,

        # APIs
        storage.path + '/api/chronos/sync', controllers.chronos.chronos,
        storage.path + '/api/chronos/update', controllers.chronos.policy_update_handler,
        storage.path + '/api/chronos/event', controllers.chronos.event_handler,
        storage.path + '/api/chronos/resume', controllers.chronos.resume_game,

        #REST
        storage.path + '/score_rest', controllers.score.score_rest,
        storage.path + '/incident_rest(/?)(.+)', controllers.incident.incident_rest,
        storage.path + '/incident_rest', controllers.incident.incident_rest,
        storage.path + '/history_rest', controllers.policy_history.history_rest,

        #SPA
        storage.path + '/login_spa', controllers.user_spa.account,
        #SPA API
        storage.path + '/api/user_spa/account(/?)(.+)', controllers.user_spa.account,
        storage.path + '/api/user_spa/account', controllers.user_spa.account,
        storage.path + '/api/user_spa/password(/?)(.+)', controllers.user_spa.password,
        storage.path + '/password_spa', controllers.user_spa.password,
        storage.path + '/api/characters', controllers.characters.characters,
        storage.path + '/api/score_frame', controllers.policy_history.score_frame
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
