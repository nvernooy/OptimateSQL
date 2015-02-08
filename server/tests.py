import unittest
from pyramid import testing

# Testing the pyramid models
class OptimateObjectModelTests(unittest.TestCase):
    """
    Test the OptimateObject from the models
    """

    def _getTargetClass(self):
        from .models import OptimateObject
        return OptimateObject

    def _makeOne(self, name = "TestName", desc = "Test Description", parent = "0"):
        return self._getTargetClass()(name, desc, parent)

    def test_constructor(self):
        instance = self._makeOne()
        self.assertEqual(instance.Name, "TestName")

class RootModelTests(unittest.TestCase):
    """
    Test the RootModel Object from the models
    """

    def _getTargetClass(self):
        from .models import RootModel
        return RootModel

    def _makeOne(self):
        return self._getTargetClass()()

    def test_constructor(self):
        instance = self._makeOne()
        self.assertEqual(instance.ID, "0")

class ProjectModelTests(unittest.TestCase):
     """
    Test the Project Object from the models
    """

    def _getTargetClass(self):
        from .models import Project
        return Project

    def _makeOne(self, name = "TestProjectName", desc = "Test Description", parent = "0"):
        return self._getTargetClass()(name, desc, parent)

    def test_constructor(self):
        instance = self._makeOne()
        self.assertEqual(instance.Name, "TestProjectName")


class BudgetGroupModelTests(unittest.TestCase):
     """
    Test the BudgetGroup Object from the models
    """

    def _getTargetClass(self):
        from .models import BudgetGroup
        return BudgetGroup

    def _makeOne(self, name = "TestBudgetGroupName", desc = "Test Description", parent = "0"):
        return self._getTargetClass()(name, desc, parent)

    def test_constructor(self):
        instance = self._makeOne()
        self.assertEqual(instance.Name, "TestBudgetGroupName")

class BudgetItemModelTests(unittest.TestCase):
     """
    Test the BudgetItem Object from the models
    """

    def _getTargetClass(self):
        from .models import BudgetItem
        return BudgetItem

    def _makeOne(self, name = "TestBudgetItemName", desc = "Test Description", quan=10, rate=5, parent = "0", ):
        return self._getTargetClass()(name, desc, quan, rate, parent)

    def test_constructor(self):
        instance = self._makeOne()
        self.assertEqual(instance.Name, "TestBudgetItemName")

class AppmakerTests(unittest.TestCase):
     """
    Test the appmaker method
    """

    def _callFUT(self, zodb_root):
        from .models import appmaker
        return appmaker(zodb_root)

    def test_it(self):
        root = {}
        self._callFUT(root)
        self.assertNotEqual(len(root['app_root'].items()), 0)

class ChildViewTests(unittest.TestCase):
    """
    Test if the childview returns a non empty list
    """

    def _getTargetClass(self):
        from .models import OptimateObject
        return OptimateObject

    def _makeOne(self, name = "TestName", desc = "Test Description", parent = "0"):
        return self._getTargetClass()(name, desc, parent)

    def test_it(self):
        from .views import childview
        context = testing.DummyResource(Subitem={"1": self._makeOne()})
        request = testing.DummyRequest()
        response = childview(context, request)
        self.assertNotEqual(len(response), 0)

class AddItemViewTests(unittest.TestCase):
    """
    Test if the additemview returns ok
    """

    def _getTargetClass(self):
        from .models import OptimateObject
        return OptimateObject

    def _makeOne(self, name = "TestName", desc = "Test Description", parent = "0"):
        return self._getTargetClass()(name, desc, parent)

    def _callFUT(self, context, request):
        from .views import additemview
        return additemview(context, request)

    def test_success(self):
        context =self._makeOne()
        request = testing.DummyRequest()
        info = self._callFUT(context, request)
        self.assertEqual(info.code, 200)

class DeleteItemViewTests(unittest.TestCase):
    """
    Test if the deleteitemview returns 404 when the item is not found
    """

    def _getTargetClass(self):
        from .models import OptimateObject
        return OptimateObject

    def _makeOne(self, name = "TestName", desc = "Test Description", parent = "0"):
        return self._getTargetClass()(name, desc, parent)

    def _callFUT(self, context, request):
        from .views import deleteitemview
        return deleteitemview(context, request)

    def test_fail(self):
        context = self._makeOne()
        request = testing.DummyRequest(json_body={'ID': 1})
        info = self._callFUT(context, request)
        self.assertEqual(info.code, 404)

# class PasteItemViewTests(unittest.TestCase):
    # """
    # The pasteitemview is giving an error due to ZODB connection issues
    # """
#     def _getTargetClass(self):
#         from .models import OptimateObject
#         return OptimateObject

#     def _makeOne(self, name = "TestName", desc = "Test Description", parent = "0"):
#         return self._getTargetClass()(name, desc, parent)

#     def _callFUT(self, context, request):
#         from .views import pasteitemview
#         return pasteitemview(context, request)

#     def test_success(self):
#         context = self._makeOne()
#         request = testing.DummyRequest()
#         info = self._callFUT(context, request)
#         self.assertTrue(info['success'])


class FunctionalTests(unittest.TestCase):
    """
    Test if the different url addresses return the correct http codes
    """

    def setUp(self):
        import tempfile
        import os.path
        from . import main
        self.tmpdir = tempfile.mkdtemp()

        dbpath = os.path.join( self.tmpdir, 'test.db')
        uri = 'file://' + dbpath
        settings = { 'zodbconn.uri' : uri ,
                     'pyramid.includes': ['pyramid_zodbconn', 'pyramid_tm'] }

        app = main({}, **settings)
        self.db = app.registry._zodb_databases['']
        from webtest import TestApp
        self.testapp = TestApp(app)

    def tearDown(self):
        import shutil
        self.db.close()
        shutil.rmtree( self.tmpdir )

    def test_root(self):
        response = self.testapp.get('/', status=200)
        self.assertNotEqual(len(response.body), 0)

    def test_Add(self):
        res = self.testapp.get('/add', status=200)
        self.assertTrue(b'OK' in res.body)

    def test_Delete(self):
        res = self.testapp.get('/1/delete', status=404)
        self.assertTrue(b'Not Found' in res.body)

    def test_Paste(self):
        res = self.testapp.get('/1/paste', status=404)
        self.assertTrue(b'Not Found' in res.body)

    def test_unexisting_page(self):
        res = self.testapp.get('/SomePage', status=404)
        self.assertTrue(b'Not Found' in res.body)
