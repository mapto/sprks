__author__ = 'zcabh_000'

import web


class mysession:
    store = web.session.DiskStore('sessions')