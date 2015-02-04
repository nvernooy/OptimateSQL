"""
views.py sets up the view in the web file
it uses json as a renderer
the only response is a data structure containing a hierarchy
of the cost estimate items
"""

from pyramid.view import view_config
from pyramid.response import Response
from models import RootModel, Project, BudgetGroup, BudgetItem
from models import appmaker
from pyramid_zodbconn import get_connection
from persistent import Persistent
import transaction


@view_config(context=RootModel, renderer='json')
@view_config(context=Project, renderer='json')
@view_config(context=BudgetGroup, renderer='json')
@view_config(context=BudgetItem, renderer='json')
def childview(context, request):
    """
    This view is for when the user requests the children of an item.
     It uses any of the obejcts as it's context, it extracts the subitem (children) from the object,
     adds it to a list and returns it to the JSON renderer
    """

    childrenlist = []
    for key in context.Subitem.keys():
        childrenlist.insert(len(childrenlist), {
            "Name":context.Subitem[key].Name,
            "Description":context.Subitem[key].Description,
            "Subitem":[], "ID":context.Subitem[key].ID,
            # "Parent": context.Subitem[key].__parent__})
            "Path": context.Subitem[key].Path})

    return childrenlist

@view_config(name = "add",context=RootModel, renderer='json')
@view_config(name = "add",context=Project, renderer='json')
@view_config(name = "add",context=BudgetGroup, renderer='json')
@view_config(name = "add",context=BudgetItem, renderer='json')
def additemview(context, request):
    """
    The postview is called when an http POST request is sent from the client.
    The method find the item that called the POST and adds a child to that parent.
    """
    print "we're in add context view"

    if request.method == 'OPTIONS':
        return {"success" : True}
    else:
        print "adding to item"
        bg = BudgetGroup("TestBG", "TestBG Description", context.ID)
        context.addItem(bg.ID, bg)

        print "commiting"
        import transaction
        transaction.commit()

        print "returning success"
        return {"success" : True}


@view_config(name = "delete",context=RootModel, renderer='json')
@view_config(name = "delete",context=Project, renderer='json')
@view_config(name = "delete",context=BudgetGroup, renderer='json')
@view_config(name = "delete",context=BudgetItem, renderer='json')
def deleteitemview(context, request):
    """
    The postview is called when an http POST request is sent from the client.
    The method find the item that called the POST and adds a child to that parent.
    """
    print "we're in delete context view"

    if request.method == 'OPTIONS':
        return {"success" : True}
    else:
        data = request.json_body
        print "setting item to none"

        print context

        print "context deletion"
        print context.ID
        try:
            context.delete([data['ID']])
        except Exception, e:
            print e

        print "new context"
        print context
        # context = None
        print "commiting"
        transaction.commit()

        print "returning success"
        return {"success" : True}

@view_config(name = "paste",context=RootModel, renderer='json')
@view_config(name = "paste",context=Project, renderer='json')
@view_config(name = "paste",context=BudgetGroup, renderer='json')
@view_config(name = "paste",context=BudgetItem, renderer='json')
def additemview(context, request):
    """
    The postview is called when an http POST request is sent from the client.
    The method find the item that called the POST and adds a child to that parent.
    """
    print "we're in paste context view"

    if request.method == 'OPTIONS':
        return {"success" : True}
    else:
        print "pasting to item"

        data = request.json_body

        print data.items()
        # bg = BudgetGroup("TestBG", "TestBG Description", context.ID)
        # context.addItem(bg.ID, bg)

        # print "commiting"
        # import transaction
        # transaction.commit()

        print "returning success"
        return {"success" : True}
