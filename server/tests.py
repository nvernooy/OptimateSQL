"""
Unit test for this package
"""

import unittest


class FunctionalTests(unittest.TestCase):
    """ There is only one test case so far,
    whether the response is a json data structure"""

    def json_data(self):
        """Test if the response is a JSON object."""
        res = self.testapp.get('/', status=200)
        self.assertEqual(res.content_type, 'application/json')
