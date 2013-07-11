import random
import hashlib
import time
import datetime


class hash_utils:
    @classmethod
    def hash_password(cls, password):
        """
        Hashes password for database.
        """
        return hashlib.sha224(password).hexdigest()

    @classmethod
    def random_hex(cls):
        """
        Generates random string using parameter as salt, sha224 hashing, random integer, and returns hexdigest.
        """
        random.seed()
        return hashlib.sha224(time.asctime(time.gmtime()) + str(random.randint(1, 100000))).hexdigest()


class date_utils:

    @classmethod
    def iso8601_to_date(cls, datestamp):
        """
        Converts ISO8601 date (YYYY-MM-DD) to datetime.date object.
        """
        return (datetime.datetime.strptime(datestamp, '%Y-%m-%d')).date()