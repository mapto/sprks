import web
import session

import pages.register
import pages.secured_page
import pages.secured_page2
import pages.login
import pages.pwrecovery
import pages.pwrequest
import pages.code_get_post

urls = ('/', pages.login.login,
        '/login', pages.login.login,
        '/register', pages.register.register,
        '/secured_page', pages.secured_page.secured_page,
        '/secured_page2', pages.secured_page2.secured_page,
        '/pwrecovery/(.*)', pages.pwrecovery.pwrecovery,
        '/pwrecovery', pages.pwrecovery.pwrecovery,
        '/pwrequest', pages.pwrequest.pwrequest,
        '/pwpolicy', pages.code_get_post.index # this URL is also being used in templates/index.html for AJAX services
)

if __name__ == "__main__":
    app = web.application(urls, globals())
    if web.config.get('_session') is None:
        session.mysession.session = web.session.Session(app, session.mysession.store, initializer={'user': 'anonymous', 'loggedin': False, 'id': 0})
        web.config._session = session
    else:
        session.mysession.session = web.config._session
    app.run()