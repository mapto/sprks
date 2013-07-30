__author__ = 'mruskov'

import os


class TestWorkEnv:
    """
    Tests localsys preferences
    """

    def test_working_dir(self):
        assert os.getcwd() == os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
