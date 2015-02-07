"""
views.py sets up the view in the web file
it uses json as a renderer
the only response is a data structure containing a hierarchy
of the cost estimate items
"""

from pyramid.view import view_config
from pyramid.response import Response
from models import OptimateObject, RootModel, Project, BudgetGroup, BudgetItem
from models import appmaker
from pyramid_zodbconn import get_connection
from persistent import Persistent
import transaction
import pdb
from BTrees.OOBTree import OOBTree

@view_config(context=OptimateObject, renderer='json')
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

@view_config(name="add", context=OptimateObject, renderer='json')
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
        newnode = OptimateObject("TestObject", "Test Object Description", context.ID)
        context.addItem(newnode.ID, newnode)

        # bg = BudgetGroup("TestBG", "TestBG Description", context.ID)
        # context.addItem(bg.ID, bg)

        print "commiting"
        transaction.commit()

        print "returning success"
        return {"success" : True}

@view_config(name = "delete", context=OptimateObject, renderer='json')
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

        print context

        print "context deletion"
        context.delete(data['ID'])

        print "new context"
        print context
        # context = None
        print "commiting"
        transaction.commit()

        print "returning success"
        return {"success" : True}

@view_config(name = "paste",context=OptimateObject, renderer='json')
@view_config(name = "paste",context=RootModel, renderer='json')
@view_config(name = "paste",context=Project, renderer='json')
@view_config(name = "paste",context=BudgetGroup, renderer='json')
@view_config(name = "paste",context=BudgetItem, renderer='json')
def pasteitemview(context, request):
    """
    The postview is called when an http POST request is sent from the client.
    The method find the item that called the POST and adds a child to that parent.
    """
    print "we're in paste context view"

    if request.method == 'OPTIONS':
        return {"success" : True}
    else:
        print "pasting to item"

        conn = get_connection(request)
        app_root = appmaker(conn.root())

        print "getting path"
        path = request.json_body["Path"]
        path = path[1:-1]
        pathlist = path.split ("/")

        copy = app_root

        print "getting node to be copied"
        for pid in pathlist:
            copy = copy[pid]

        print "rebuilding"
        # need to rebuild target with new id and path
        try:
            paste = rebuild (copy, context.ID)
            print paste
            context.addItem (paste.ID, paste)

            print "commiting"
            transaction.commit()
        except Exception, e:
            print e
            raise e

        print "returning success"
        return {"success" : True}

def rebuild(copy, parentid):
    """ Recursively rebuilds the object and its children."""
    copiedobject = OptimateObject(copy.Name, copy.Description, parentid)
    if copy.Subitem != []:
        for key, value in copy.items():
            copiedchildren = rebuild(value, copiedobject.ID)
            copiedobject.addItem(copiedchildren.ID, copiedchildren)

    return copiedobject

