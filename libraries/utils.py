__author__ = 'Horace'

import random
import hashlib


class hash_utils:

    @staticmethod
    def hash_password(password):
        """
        Hashes password for database.
        """
        return hashlib.sha224(password).hexdigest()

    @staticmethod
    def random_hex(salt):
        random.seed()
        rand = hashlib.sha224(salt+str(random.randint(1, 100000))).hexdigest()