"""
This is the Integration test for Kong authChecker plugin
"""
import unittest
import http.client


class PluginTestCase(unittest.TestCase):
    """Summary

    Attributes:
        conn (TYPE): Description
        payload (str): Description
    """

    def setUp(self):
        """Summary
        """
        self.conn = http.client.HTTPConnection("localhost:8000")
        self.payload = ""

    def test_good_auth(self):
        """Summary
        """
        headers = {'token': "bWFpbEBuaXRpbmtoYW5uYS5jb206YmVzdFBhc3N3MHJk"}
        self.conn.request("GET", "/anything", self.payload, headers)
        res = self.conn.getresponse()
        res.read()
        self.assertTrue(res.status == 200)

    def test_bad_auth(self):
        """Summary
        """
        headers = {'token': "bWFpbEBuaXRpbmtoYW5uYS5jb206d3JvbmdQYXNzdzByZA=="}
        self.conn.request("GET", "/anything", self.payload, headers)
        res = self.conn.getresponse()
        res.read()
        self.assertTrue(500 > res.status >= 400)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
