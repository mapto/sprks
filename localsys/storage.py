import web
import importlib


try:
    settings = importlib.import_module('settings')
    # Assuming that only MySQL is used
    db = web.database(
        dbn='mysql',
        user=getattr(settings, 'dbuser'),
        pw=getattr(settings, 'dbpw'),
        db=getattr(settings, 'dbname', 'sprks'),
        host=getattr(settings, 'host', '127.0.0.1'),
        port=getattr(settings, 'port', 3306)
    )
    path = getattr(settings, 'path', '')
except ImportError, AttributeError:
    # Default DB credentials
    db = web.database(
        user='root',
        pw='1234',
        db='sprks',
        host='127.0.0.1',
        dbn='mysql',
        #user='seccompman', #for connection to orpheus server
        #pw='ke:p17loadeD', #for connection to orpheus server
        #db='sprks-zhanelya', #for connection to orpheus server
        port=3306
    )
    path = ''