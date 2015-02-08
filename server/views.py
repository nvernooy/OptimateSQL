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
from pyramid.httpexceptions import HTTPOk, HTTPNotFound

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
            "Subitem":[],
            "ID":context.Subitem[key].ID,
            "Path": context.Subitem[key].Path})

    return childrenlist

@view_config(name="add", context=OptimateObject, renderer='json')
@view_config(name = "add",context=RootModel, renderer='json')
@view_config(name = "add",context=Project, renderer='json')
@view_config(name = "add",context=BudgetGroup, renderer='json')
@view_config(name = "add",context=BudgetItem, renderer='json')
def additemview(context, request):
    """
    The additemview is called when an http POST request is sent from the client.
    The method adds a built in new OptimateObject to the current node.
    """

    if request.method == 'OPTIONS':
        return {"success" : True}
    else:
        print "adding to item"
        newnode = OptimateObject("TestObject", "Test Object Description", context.ID)
        context.addItem(newnode.ID, newnode)

        transaction.commit()

        return HTTPOk()

@view_config(name = "delete", context=OptimateObject, renderer='json')
@view_config(name = "delete",context=RootModel, renderer='json')
@view_config(name = "delete",context=Project, renderer='json')
@view_config(name = "delete",context=BudgetGroup, renderer='json')
@view_config(name = "delete",context=BudgetItem, renderer='json')
def deleteitemview(context, request):
    """
    The deleteitemview is called using the address from the node to be deleted.
    The node ID is sent in the request, and it is deleted from the context.
    The try block catches if a node is not found, and returns a 404 http exception
    """

    if request.method == 'OPTIONS':
        return {"success" : True}
    else:
        data = request.json_body

        print "context deletion"
        # If the item is not found, an HTTP 404 status is returned
        try:
            context.delete(data['ID'])
        except Exception, e:
            return HTTPNotFound()

        transaction.commit()

        return HTTPOk()

@view_config(name = "paste",context=OptimateObject, renderer='json')
@view_config(name = "paste",context=RootModel, renderer='json')
@view_config(name = "paste",context=Project, renderer='json')
@view_config(name = "paste",context=BudgetGroup, renderer='json')
@view_config(name = "paste",context=BudgetItem, renderer='json')
def pasteitemview(context, request):
    """
    The pasteitemview is sent the path of the node that is to be copied.
    That node is then found in the zodb, rebuilt with a new ID and path,
    and added to the current node.
    """

    if request.method == 'OPTIONS':
        return {"success" : True}
    else:
        print "pasting to item"
        pathlist = request.json_body["Path"][1:-1].split ("/")
        app_root = appmaker( get_connection(request).root())
        copy = app_root

        for pid in pathlist:
            copy = copy[pid]

        # need to rebuild target with new id and path
        paste = rebuild (copy, context.ID)
        context.addItem (paste.ID, paste)
        transaction.commit()

        return HTTPOk()

def rebuild(copy, parentid):
    """
    Recursively rebuilds the object and its children.
    The data from the old object is copied to the new object,
    which automatically regenerates an ID and path.
    The finished node with all its children returned.
    """

    copiedobject = OptimateObject(copy.Name, copy.Description, parentid)
    if copy.Subitem != []:
        for key, value in copy.items():
            copiedchildren = rebuild(value, copiedobject.ID)
            copiedobject.addItem(copiedchildren.ID, copiedchildren)

    return copiedobject

