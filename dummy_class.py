import web
import register
import dummy_index
import session
import secured_page
import secured_page2
import login

urls = (
    '/', dummy_index.index,
         '/login', login.login,
        '/register', register.register,
        '/secured_page', secured_page.secured_page,
        '/secured_page2', secured_page2.secured_page
)

if __name__ == "__main__":
    app = web.application(urls, globals())
    if web.config.get('_session') is None:
        session.mysession.session = web.session.Session(app, session.mysession.store, initializer={'user': 'anonymous', 'loggedin': False})
        web.config._session = session
    else:
        session.mysession.session = web.config._session
    app.run()