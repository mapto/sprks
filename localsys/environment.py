import web
import datetime
from models.users import users_model
from web import ctx
from localsys import storage


class context:
    """
    Caches current user details.
    """

    @staticmethod
    def cache():
        """
        Returns a cache specific to the context (http request)
        """
        try:
            return getattr(ctx, 'cache')
        except AttributeError:
            ctx.cache = {}
            return ctx.cache

    @staticmethod
    def flush_cache():
        context.cache().clear()

    @staticmethod
    def user_id():
        """
        If HTTP Authorization header, returns user authorized, or 0.
        Else if user sesion in progress, returns session user_id, or 0.
        """
        user_id = context.cache().get('user_id')
        if user_id is None:
            context.cache()['user_id'] = users_model.authorize()
            return context.cache()['user_id']
        return user_id

    @staticmethod
    def username():
        """
        If HTTP Authorization header, returns user authorized, or empty string.
        Else if user session in progress, returns session username, or empty string.
        """
        username = context.cache().get('username')
        if username is None:
            context.cache()['username'] = users_model.get_username(context.user_id())
            return context.cache()['username']
        return username


start_date = datetime.date(2014, 1, 6)


def get_start_time():
    return start_date


render_globals = {
    'datetime': datetime,
    'get_start_time': get_start_time,
    'user_id': context.user_id,
    'username': context.username,
    'path': storage.path
}

render = web.template.render('views/', base='skeleton', globals=render_globals)
