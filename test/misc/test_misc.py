__author__ = 'Horace'

from mock import patch
from mock import Mock
import localsys


class TestMock:
    """
    Misc tests for checking functionality of the Mock UT framework.
    """

    mock_db = Mock()

    @patch.object(localsys.datstore, 'db', mock_db)
    def test_patch_object(self):
        assert self.mock_db == localsys.datastore.db