"""
Now separated settings from environment.
Environment takes care of the system objects that need to be used by many modules
"""

__author__ = 'mruskov'

import web
import session
from datetime import datetime
# from controllers.timeline import get_start_time
import importlib

def get_start_time():
    return datetime.strptime("2014-1-6 9", "%Y-%m-%d %H") # 9am on 6 January 2014

# Now assuming that views directory is fixed.
# It is invisible to the code which renderer is used
# the only difference is in the import line, e.g. use it as follows:
#
#   from environment import render_private as render
#   render.score(8,2,3)
#
globals = {
    'datetime': datetime,
    'get_start_time': get_start_time
} # Parameters for private render
render_private = web.template.render('views/', base='index_private', globals=globals)
render_public = web.template.render('views/', base='index_public')

try:
    settings = importlib.import_module('settings')
    # Assuming that only MySQL is used
    db = web.database(dbn='mysql',
        user=getattr(settings,'dbuser'),
        pw=getattr(settings,'dbpw'),
        db=getattr(settings,'dbname'))
except ImportError, AttributeError:
    # Default DB credentials
    db = web.database(host='127.0.0.1',
        dbn='mysql',
        user='root',
        pw='1234',
        db='sprks')

