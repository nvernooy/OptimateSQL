"""
So far only the pyramid views and their functions are being tested.
That is: Child view
        Add view
        Delete view
        Paste view
"""

import unittest
import transaction
from pyramid import testing
from .models import DBSession

def _initTestingDB():
    """
    Build a database with default data
    """

    from sqlalchemy import create_engine
    from .models import (
        DBSession,
        Project,
        BudgetGroup,
        BudgetItem,
        Base
        )
    engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)
    DBSession.configure(bind=engine)
    with transaction.manager:
            project = Project(ID='1',
                                Name="TestName",
                                Description="Test Description",
                                ParentID='0')

            budgetgroup = BudgetGroup(ID='2',
                                Name="TestBGName",
                                Description="Test BG Description",
                                ParentID=project.ID)

            budgetitem = BudgetItem(ID='3',
                                Name="TestBIName",
                                Description="Test BI Description",
                                Quantity=10,
                                Rate=5,
                                ParentID=budgetgroup.ID)

            budgetgroup.Children.append(budgetitem)
            project.Children.append(budgetgroup)
            DBSession.add(project)

    return DBSession


def _registerRoutes(config):
    config.add_route('root', '/')
    config.add_route('childview', '/{parentid}/')
    config.add_route('addview', '/{id}/add')
    config.add_route('deleteview', '/{id}/delete')
    config.add_route('pasteview', '/{id}/paste')

class TestRootviewSuccessCondition(unittest.TestCase):
    """
    Test if the Root view functions correctly.
    It also calls the childview but without a url path,
    the default root id '0' is then used in the view
    """

    def setUp(self):
        self.session = _initTestingDB()
        self.config = testing.setUp()

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def _callFUT(self, request):
        from .views import childview
        return childview(request)

    def test_it(self):
        _registerRoutes(self.config)
        request = testing.DummyRequest()
        response = self._callFUT(request)

        # assert returns true if the child object of the root has Name 'TestName'
        self.assertEqual(response[0]['Name'], 'TestName')

class TestChildviewSuccessCondition(unittest.TestCase):
    """
    Test if the childview functions correctly with any other id.
    """

    def setUp(self):
        self.session = _initTestingDB()
        self.config = testing.setUp()

    def tearDown(self):
        self.session.remove()
        testing.tearDown()

    def _callFUT(self, request):
        from .views import childview
        return childview(request)

    def test_it(self):
        _registerRoutes(self.config)
        request = testing.DummyRequest()
        request.matchdict['parentid'] = '1'
        response = self._callFUT(request)

        # true if the child object of parent id '1' has Name 'TestBGName'
        self.assertEqual(response[0]['Name'], 'TestBGName')

class TestAddviewSuccessCondition(unittest.TestCase):
    """
    Test if the additemview functions correctly.
    Using default data and adding it as the child of one of the objects.
    """

    def setUp(self):
        self.session = _initTestingDB()
        self.config = testing.setUp()

    def tearDown(self):
        self.session.remove()
        testing.tearDown()

    def _callFUT(self, request):
        from .views import additemview
        return additemview(request)

    def test_it(self):
        _registerRoutes(self.config)

        # Add the default data using json in the request
        request = testing.DummyRequest(json_body={
                                                'Name':'AddingName',
                                                'Description':'Adding test item',
                                                'Type':'budgetgroup'}
                                        )
        request.matchdict= {'id':'3'}
        response = self._callFUT(request)

        # assert if the response from the add view is OK
        self.assertEqual(response.code, 200)

        # Create another request for the child of the node added to
        request = testing.DummyRequest()
        request.matchdict= {'parentid': '3'}
        from .views import childview
        response = childview(request)

        # true if the name of the child added to the node is 'AddingName'
        self.assertEqual(response[0]['Name'], 'AddingName')

class TestDeleteviewSuccessCondition(unittest.TestCase):
    """
    Test if the delete view functions correctly and deletes the node
    specified by the request.
    """

    def setUp(self):
        self.session = _initTestingDB()
        self.config = testing.setUp()

    def tearDown(self):
        self.session.remove()
        testing.tearDown()

    def _callFUT(self, request):
        from .views import deleteitemview
        return deleteitemview(request)

    def test_it(self):
        _registerRoutes(self.config)
        request = testing.DummyRequest()
        request.matchdict= {'id':'2'}
        response = self._callFUT(request)

        # true if the response from deleteview is OK
        self.assertEqual(response.code, 200)

        request = testing.DummyRequest()
        request.matchdict= {'parentid': '2'}
        from .views import childview
        response = childview(request)

        # test again that the children of the parent is now zero
        self.assertEqual(len(response), 0)

class TestPasteviewSuccessCondition(unittest.TestCase):
    """
    Test that the paste functions correctly with pasting from a
    default node to another one.
    """

    def setUp(self):
        self.session = _initTestingDB()
        self.config = testing.setUp()

    def tearDown(self):
        self.session.remove()
        testing.tearDown()

    def _callFUT(self, request):
        from .views import pasteitemview
        return pasteitemview(request)

    def test_it(self):
        _registerRoutes(self.config)
        # set the default node to be copied
        request = testing.DummyRequest(json_body={
                                                'Path': '/3/'}
                                        )
        # set the node to be pasted into
        request.matchdict= {'id':'1'}
        response = self._callFUT(request)

        # true if the response from paste view is OK
        self.assertEqual(response.code, 200)

        request = testing.DummyRequest()
        request.matchdict= {'parentid': '1'}
        from .views import childview
        response = childview(request)

        # do another test to see if the children of the parent is now two
        self.assertEqual(len(response), 200)
