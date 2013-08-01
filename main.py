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
import controllers.spa
import controllers.user
import controllers.characters

urls = (
    storage.path + '', controllers.spa.spa,
    storage.path + '/', controllers.spa.spa,
    storage.path + '/score/multiple', controllers.score.multiple_score,

    # API
    storage.path + '/api/user/account/(.+)', controllers.user.account,
    storage.path + '/api/user/account', controllers.user.account,
    storage.path + '/api/user/password/(.+)', controllers.user.password,
    storage.path + '/api/chronos/update', controllers.chronos.policy_update_handler,
    storage.path + '/api/chronos/event', controllers.chronos.event_handler,
    storage.path + '/api/chronos/resume', controllers.chronos.resume_game,
    storage.path + '/api/characters', controllers.characters.characters,
    storage.path + '/api/score_frame', controllers.policy_history.score_frame,
    storage.path + '/api/score', controllers.score.score_rest,
    storage.path + '/api/incident/(.+)', controllers.incident.incident_rest,
    storage.path + '/api/incident', controllers.incident.incident_rest,
    storage.path + '/api/history', controllers.policy_history.history_rest
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
    application = app.wsgifunc()  # when called from Apache, use WSGI
