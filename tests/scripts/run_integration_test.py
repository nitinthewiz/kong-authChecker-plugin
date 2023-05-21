"""
This is the Integration test for Kong authChecker plugin
"""
import unittest
import http.client


class AuthCheckerPluginIntegrationTestCase(unittest.TestCase):
    """Summary

    Attributes:
        conn (http.client.HTTPConnection): The HTTP connection to Kong.
        payload (str): An empty payload, because we're only focused on
                       headers for now.
    """

    def setUp(self):
        """Set up the test case by creating an HTTP connection to Kong
           and initializing the payload to blank.
        """
        self.conn = http.client.HTTPConnection("localhost:8000")
        self.payload = ""

    def test_good_auth(self):
        """Test the authentication with valid credentials.

        The test sends an HTTP GET request with a valid token header and asserts that the response
        status code is 200 (OK).
        """
        headers = {'token': "bWFpbEBuaXRpbmtoYW5uYS5jb206YmVzdFBhc3N3MHJk"}
        self.conn.request("GET", "/anything", self.payload, headers)
        res = self.conn.getresponse()
        res.read()
        self.assertTrue(res.status == 200)

    def test_bad_auth(self):
        """Test the authentication with invalid credentials.

        The test sends an HTTP GET request with an invalid token header and asserts that the response
        status code is between 400 (Bad Request) and 499 (Client Closed Request).
        Currently, the bad response is hardcoded to 401 (Unauthorized).
        """
        headers = {'token': "bWFpbEBuaXRpbmtoYW5uYS5jb206d3JvbmdQYXNzdzByZA=="}
        self.conn.request("GET", "/anything", self.payload, headers)
        res = self.conn.getresponse()
        res.read()
        self.assertTrue(500 > res.status >= 400)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
