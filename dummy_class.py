import web
import session

import controllers.register
import controllers.secured_page
import controllers.secured_page2
import controllers.login
import controllers.pwrecovery
import controllers.pwrequest
import controllers.code_get_post

urls = ('/', controllers.login.login,
        '/login', controllers.login.login,
        '/register', controllers.register.register,
        '/secured_page', controllers.secured_page.secured_page,
        '/secured_page2', controllers.secured_page2.secured_page,
        '/pwrecovery/(.*)', controllers.pwrecovery.pwrecovery,
        '/pwrecovery', controllers.pwrecovery.pwrecovery,
        '/pwrequest', controllers.pwrequest.pwrequest,
        '/pwpolicy', controllers.code_get_post.index # this URL is also being used in views/index.html for AJAX services
)

if __name__ == "__main__":
    app = web.application(urls, globals())
    if web.config.get('_session') is None:
        session.mysession.session = web.session.Session(app, session.mysession.store, initializer={'user': 'anonymous', 'loggedin': False, 'id': 0})
        web.config._session = session
    else:
        session.mysession.session = web.config._session
    app.run()