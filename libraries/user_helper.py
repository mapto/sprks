from localsys import storage


class authenticate:

    @staticmethod
    def check():
        """
        Returns user_id if client is authorized, else 0. Stub to allow other methods of authorization (eg OAuth).
        """
        return storage.session.user_id
