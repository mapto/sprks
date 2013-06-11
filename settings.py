__author__ = 'mysql' # change the value of this line to make it match your user

import web

class settings:
    """ deployment settings
        This class serves as an abstraction from the exact deployment.
        It is also is useful to keep our passwords locally and this way avoid sharing them with others
        This object:
        * stores personal credentials
        * makes a connection to the database
        * points to local files, e.g. templates to render
    """
    credentials = {
        'sqlite':  {'user': 'not-used', 'pw': '', 'db': ''}, # sqlite does not require credentials
        'mysql':   {'user': 'root', 'pw': '1234', 'db': 'sprks'},
        'mruskov': {'user': 'root', 'pw': '1234', 'db': 'sprks'}
        # add a line with the name of your configuration
    }

    created = False

    def __init__(self, profile=__author__):
        """ Lazy initialization upon request.
            Do nothing if already exists.
            See http://en.wikipedia.org/wiki/Singleton_pattern

            Parameters:
            * profile is same as owner of local file if not specified
        """
        if not self.created:
            self.created = True

            # add a case here if you need some specific setup for your development copy or installation
            if profile == 'sqlite':
                self.db = web.database(dbn='sqlite', db=self.credentials[profile]['db'])
                self.populate()
            else:
                self.db = web.database(
                    dbn='mysql',
                    user=self.credentials[profile]['user'],
                    pw=self.credentials[profile]['pw'],
                    db=self.credentials[profile]['db']
                )

            self.render = render = web.template.render('templates/')

    def populate(self):
        ''' presumes that database is already connected
            OBSOLETE
        '''
        db = self.db

#       use this if table needs to be created
        db.query('CREATE TABLE users (id INT NOT NULL PRIMARY KEY, username varchar(256), password varchar(256), email varchar(256));')
        db.query("INSERT INTO users VALUES (1, 'mapto', '', 'mapto@ko64eto.com');")

#       use this if table needs to be created
#        db.query('CREATE TABLE pw_policy(id INT NOT NULL PRIMARY KEY, plen INT, psets INT, pdict BOOL, phist INT, prenew INT, pattempts BOOL, pautorecover BOOL);')
#        db.query('CREATE TABLE pw_policy (idpolicy int(11) NOT NULL AUTO_INCREMENT,plen int(11) NOT NULL,psets int(11) NOT NULL,pdict tinyint(4) NOT NULL,phist int(11) NOT NULL,prenew int(11) NOT NULL,pattempts tinyint(4) NOT NULL,pautorecover tinyint(4) NOT NULL,userid int(11) NOT NULL,PRIMARY KEY (idpolicy);')
        db.query('CREATE TABLE pw_policy (idpolicy int(11) NOT NULL,plen int(11) NOT NULL,psets int(11) NOT NULL,pdict tinyint(4) NOT NULL,phist int(11) NOT NULL,prenew int(11) NOT NULL,pattempts tinyint(4) NOT NULL,pautorecover tinyint(4) NOT NULL,userid int(11) NOT NULL);')
#       use this if table needs to be filled with values
