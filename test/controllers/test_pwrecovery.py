__author__ = 'Horace'

import web
import pytest
from mock import patch, MagicMock
from controllers.pwrecovery import *


class TestGetRequest:
    mock_users_model = MagicMock()
    mock_render_public = MagicMock()

    @patch('models.users.users_model.pwrecovery_status', mock_users_model.pwrecovery_status)
    def test_invalid_recovery_ticket(self):
        """
        Tests GET request to pwrecovery.py with empty string as ticket.
        """
        self.mock_users_model.pwrecovery_status.return_value = ''

        assert pwrecovery().GET('') == "Invalid password recovery request"

    @patch('models.users.users_model.pwrecovery_status', mock_users_model.pwrecovery_status)
    @patch('environment.render_public.pwrecovery', mock_render_public.pwrecovery)
    def test_valid_recovery_ticket(self):
        """
        Tests GET request to pwrecovery.py with valid ticket.
        """

        def mock_render(arg):
            return 'render.pwrecovery ' + arg

        self.mock_users_model.pwrecovery_status.return_value = 'dummy_username1'
        self.mock_render_public.pwrecovery.side_effect = mock_render

        assert pwrecovery().GET('') == "render.pwrecovery dummy_username1"


class TestPostRequest:

    mock_web_ctx = MagicMock()

    # TODO patches cause errors

    # @patch('web.ctx.env.get', mock_web_ctx.env.get)
    # @patch.object(web.ctx, 'host', mock_web_ctx.host)
    def test_bad_post_referer(self):
        """
        Tests for rejection of user request if http referer doesn't match /pwrecovery.
        """

        self.mock_web_ctx.env_get.return_value = 'BAD_REFERER'
        self.mock_web_ctx.host.return_value = 'CURRENT_HOST'

        # pwrecovery().POST()

        # pytest.raises(Exception)