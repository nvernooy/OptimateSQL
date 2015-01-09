"""
Unit test for this package
"""

import unittest

from pyramid import testing

class FunctionalTests(unittest.TestCase):

	""" There is only one test case, whether the response is a json data structure"""
    def json_data(self):
        res = self.testapp.get('/', status=200)
        self.assertEqual(res.content_type, 'application/json')
