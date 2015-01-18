import unittest

from pyramid import testing


class ServerViewTests(unittest.TestCase):
    """Test server response."""

    def setUp(self):
        """Set up testing configuration"""
        self.config = testing.setUp()

    def tearDown(self):
        """Tear down setup"""
        testing.tearDown()

    def test_list_not_empty(self):
        """Test data is in the list"""
        import views

        request = testing.DummyRequest()
        response = views.formatdata(request)
        self.assertNotEqual(0, len(response))

    def test_data_response(self):
        """Test data sent by JSON"""
        import views

        request = testing.DummyRequest()
        response = views.formatdata(request)
        self.assertEqual("A", response[0]["Name"])


class ServerFunctionalTests(unittest.TestCase):
    """Functional tests here"""

    def setUp(self):
        """Setup enviroment"""
        from server import main
        app = main({})
        from webtest import TestApp

        self.testapp = TestApp(app)

    def test_object_json(self):
        """Test response is JSON"""
        res = self.testapp.get('/', status=200)
        self.assertEqual(res.content_type, 'application/json')