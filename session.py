__author__ = 'Dan'

import web


class mysession:
    store = web.session.DiskStore('sessions')