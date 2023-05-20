"""Summary

Attributes:
    current_dir (TYPE): Description
    parent_dir (TYPE): Description
"""
import os
import sys
import unittest
from unittest.mock import MagicMock
import responses

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir + "/plugins")
from authChecker import Plugin


class PluginTestCase(unittest.TestCase):

    """Summary

    Attributes:
        plugin (TYPE): Description
    """

    def setUp(self):
        self.plugin = Plugin({'auth_server_url': 'http://authhost.com/login'})

    @responses.activate
    def test_access_successful(self):
        """Summary
        """
        kong_mock = MagicMock()
        kong_mock.request = MagicMock()

        kong_mock.request.get_header.return_value = "dGVzdHVzZXI6cGFzc3dvcmQ="

        responses.post('http://authhost.com/login',
                       status=300, json={"accessToken": "testtoken"})

        self.plugin.access(kong_mock)
        kong_mock.service.request.set_header.assert_called_with("token",
                                                                "testtoken")

    @responses.activate
    def test_access_failure(self):
        """Summary
        """
        kong_mock = MagicMock()
        kong_mock.request = MagicMock()

        kong_mock.request.get_header.return_value = "dGVzdHVzZXI6YmFkcGFzc3dvcmQ="

        responses.post('http://authhost.com/login',
                       status=401)

        self.plugin.access(kong_mock)
        kong_mock.response.exit.assert_called_with(401, "Invalid authentication credentials")


if __name__ == '__main__':
    unittest.main()
