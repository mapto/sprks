__author__ = 'mruskov'

import os

class TestWorkEnv:
    """
    Tests system preferences
    """
    def test_working_dir(self):
        assert os.getcwd() == os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

    def test_static_files(self):
        assert os.path.isfile('static/css/bootstrap.css')
        assert os.path.isfile('static/img/glyphicons-halflings.png')
        assert os.path.isfile('static/data/pw-train-data-full.csv')
        # include other static files that are required

