__author__ = 'Horace'

from libraries.utils import *


class TestHashUtils:
    """
    Test custom password hashing and random string generators.
    """

    def setup_method(self, method):
        random.seed()
        self.random_str = hash_utils.random_hex(str(random.randint(1, 10000000)))

    def test_hash_password(self):
        assert hash_utils.hash_password('') == 'd14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f'

    def test_random_hex_len(self):
        """
        Test that the length of result of random_hex is always 56.
        """
        assert len(self.random_str) == 56

    def test_random_hex_chars(self):
        """
        Test the result of random_hex is always hex characters.
        """
        try:
            int(self.random_str, 16)
        except ValueError:
            raise AssertionError('String not composed of hex characters.')
