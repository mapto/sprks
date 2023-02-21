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
        host=getattr(settings, 'dbhost', '127.0.0.1'),
        port=getattr(settings, 'dbport', 3306)
    )
    path = getattr(settings, 'path', '')
except ImportError, AttributeError:
    # Default DB credentials
    db = web.database(
        dbn='mysql',
        user='root',
        pw='1234',
        db='sprks',
        host='127.0.0.1',
        port=3306
    )
    path = ''