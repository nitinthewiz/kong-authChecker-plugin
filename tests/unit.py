"""Unit tests for the authChecker plugin.
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


class AuthCheckerPluginUnitTestCase(unittest.TestCase):

    """Primary unit test for authChecker plugin"""

    def setUp(self):
        """Set up the test case by creating an instance of the Plugin class."""
        self.plugin = Plugin({'auth_server_url': 'http://authhost.com/login'})

    def test_access_missing_header(self):
        """Test the access method for missing header."""
        kong_mock = MagicMock()
        kong_mock.request = MagicMock()
        kong_mock.request.get_header.return_value = None

        self.plugin.access(kong_mock)
        kong_mock.response.exit.assert_called_with(401, "Invalid authentication credentials")

    def test_access_blank_header(self):
        """Test the access method for a blank header."""
        kong_mock = MagicMock()
        kong_mock.request = MagicMock()
        kong_mock.request.get_header.return_value = ""

        self.plugin.access(kong_mock)
        kong_mock.response.exit.assert_called_with(401, "Invalid authentication credentials")

    def test_access_bad_long_header_value(self):
        """Test the access method for a blank header."""
        kong_mock = MagicMock()
        kong_mock.request = MagicMock()
        kong_mock.request.get_header.return_value = "VGhpcyBpcyBhbiB1bHRyYSBsb25nIGFuZCB1dHRlcmx5\
                                                     IHVzZWxlc3Mgc3RyaW5nIHdpdGggcmVzcGVjdCB0byB0\
                                                     aGUgSlNPTiBXZWIgVG9rZW4gbG9naW4gcHJvY2Vzcy4g\
                                                     VGhlcmUgaXMgbm8gY29sb24gYW5kIHRodXMgbm8gZW1h\
                                                     aWwgYW5kIHBhc3N3b3JkIGNvbWJvLiBBbmQgeWV0LCB0\
                                                     aGUgYXV0aENoZWNrZXIgcGx1Z2luIHNob3VsZCBzdGls\
                                                     bCB3b3JrIG9uIHRoaXMgc3RyaW5nIGFuZCBub3QgYnJl\
                                                     YWsgZG93bi4="

        self.plugin.access(kong_mock)
        kong_mock.response.exit.assert_called_with(401, "Invalid authentication credentials")

    @responses.activate
    def test_bad_auth_server_response(self):
        """Test the access method for a bad response from the auth server."""
        kong_mock = MagicMock()
        kong_mock.request = MagicMock()

        kong_mock.request.get_header.return_value = "dGVzdHVzZXI6cGFzc3dvcmQ="

        responses.post('http://authhost.com/login',
                       status=403)

        self.plugin.access(kong_mock)
        kong_mock.response.exit.assert_called_with(401, "Invalid authentication credentials")

    @responses.activate
    def test_access_successful(self):
        """Test the access method for successful authentication."""
        kong_mock = MagicMock()
        kong_mock.request = MagicMock()

        kong_mock.request.get_header.return_value = "dGVzdHVzZXI6cGFzc3dvcmQ="

        responses.post('http://authhost.com/login',
                       status=200, json={"accessToken": "testtoken"})

        self.plugin.access(kong_mock)
        kong_mock.service.request.set_header.assert_called_with("token",
                                                                "testtoken")


    @responses.activate
    def test_access_successful_long_header_value(self):
        """Test the access method for successful authentication even 
        with a long header value."""
        kong_mock = MagicMock()
        kong_mock.request = MagicMock()

        kong_mock.request.get_header.return_value = "ZXh0cmFsb25nZW1haWxpZG92ZXJoZXJlQHN1cGV\
                                                     ybG9uZ2RvbWFpbm5hbWV0aGF0aXNub3RuZWNlc3\
                                                     NhcmlseXZhbGlkLmNvbTp0aGlzaXNPbmVMb25nU\
                                                     GFzc3dvcmR0aGF0R29lc09uRm9yQVdoaWxlQmVj\
                                                     YXVzZUxvbmdwYXNzd29yZHNhcmViZXR0ZXJyaWd\
                                                     odD9SaWdodD9PckFtSW1pc3Rha2VuP05vdC5TdX\
                                                     IzLg=="

        responses.post('http://authhost.com/login',
                       status=200, json={"accessToken": "testtoken"})

        self.plugin.access(kong_mock)
        kong_mock.service.request.set_header.assert_called_with("token",
                                                                "testtoken")

    @responses.activate
    def test_access_failure(self):
        """Test the access method for failed authentication."""
        kong_mock = MagicMock()
        kong_mock.request = MagicMock()

        kong_mock.request.get_header.return_value = "dGVzdHVzZXI6YmFkcGFzc3dvcmQ="

        responses.post('http://authhost.com/login',
                       status=401)

        self.plugin.access(kong_mock)
        kong_mock.response.exit.assert_called_with(401, "Invalid authentication credentials")


if __name__ == '__main__':
    unittest.main()
