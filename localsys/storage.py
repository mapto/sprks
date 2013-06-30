import web

try:
    settings = __import__('settings')
    # Assuming that only MySQL is used
    db = web.database(
        dbn='mysql',
        user=getattr(settings, 'dbuser'),
        pw=getattr(settings, 'dbpw'),
        db=getattr(settings, 'dbname', 'sprks'),
        host=getattr(settings, 'host', '127.0.0.1'),
        port=getattr(settings, 'port', 3306)
    )
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
