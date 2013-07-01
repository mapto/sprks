import random
import hashlib
import time


class hash_utils:
    @staticmethod
    def hash_password(password):
        """
        Hashes password for database.
        """
        return hashlib.sha224(password).hexdigest()

    @staticmethod
    def random_hex():
        """
        Generates random string using parameter as salt, sha224 hashing, random integer, and returns hexdigest.
        """
        random.seed()
        return hashlib.sha224(time.gmtime() + str(random.randint(1, 100000))).hexdigest()
