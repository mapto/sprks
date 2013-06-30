"""
Environment takes care of the system objects that need to be used by many modules
"""

import web
from datetime import datetime
from libraries.user_helper import auth
from models.users import users_model


def get_start_time():
    return datetime.strptime("2014-1-6 9", "%Y-%m-%d %H") # 9am on 6 January 2014


def get_user_id():
    """
    Returns current user_id if logged in, otherwise 0.
    """
    return auth().check()


def get_username():
    """
    Returns current username if logged in, otherwise empty string.
    """
    return users_model().get_username(auth().check())


globals = {
    'datetime': datetime,
    'get_start_time': get_start_time,
    'get_user_id': get_user_id,
    'get_username': get_username
}

render = web.template.render('views/', base='skeleton', globals=globals)
