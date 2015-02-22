"""
views.py sets up the view in the web file
it uses json as a renderer
the only response is a data structure containing a hierarchy
of the cost estimate items
"""

# from pyramid.view import view_config
# from pyramid.response import Response
# from models import OptimateObject, RootModel, Project, BudgetGroup, BudgetItem
# from models import appmaker
# from pyramid_zodbconn import get_connection
# from persistent import Persistent
# import transaction
# import pdb
# from BTrees.OOBTree import OOBTree
# from pyramid.httpexceptions import HTTPOk, HTTPNotFound

import re
from docutils.core import publish_parts
import sqlalchemy

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    )

from pyramid.view import view_config

from .models import (
    DBSession,
    Root,
    Project,
    BudgetGroup,
    BudgetItem,
    )


@view_config(route_name='root', renderer='json')
def rootview(request):
    # root = DBSession.query(Root).first()
    # print root
    # Base = sqlalchemy.ext.declarative.declarative_base()
    # print Base.metadata.tables.keys()
    # root = Root(ID='0')
    # DBSession.add(root)
    projectquery = DBSession.query(Project).filter_by(ParentID='0').all()
    bgquery = DBSession.query(BudgetGroup).filter_by(ParentID='0').all()
    biquery = DBSession.query(BudgetItem).filter_by(ParentID='0').all()

    rootlist = [projectquery, bgquery, biquery]

    return rootlist

# @view_config(context=OptimateObject, renderer='json')
# def childview(context, request):
#     """
#     This view is for when the user requests the children of an item.
#     It uses any of the obejcts as it's context,
#     it extracts the subitem (children) from the object,
#     adds it to a list and returns it to the JSON renderer
#     """
#     childrenlist = []
#     for key, value in context.items():
#         childrenlist.insert(len(childrenlist), {
#             "Name":value.Name,
#             "Description":value.Description,
#             "Subitem":[],
#             "ID":value.ID,
#             "Path": value.Path})
#         print "\nID: " + value.ID + "\nParent: ",
#         print value.getParent().ID

#     return childrenlist



# @view_config(name="add", context=OptimateObject, renderer='json')
# def additemview(context, request):
#     """
#     The additemview is called when an http POST request is sent from the client.
#     The method adds a new node with attributes as specified by the user
#     to the current node.
#     """

#     if request.method == 'OPTIONS':
#         return {"success" : True}
#     else:
#         print "adding to item"
#         name = request.json_body['Name']
#         desc = request.json_body['Description']
#         objecttype = request.json_body['Type']

#         if objecttype == 'project':
#             newnode = Project(name, desc, context)
#             context.addItem(newnode.ID, newnode)
#         elif objecttype == 'budgetgroup':
#             newnode = BudgetGroup(name, desc, context)
#             context.addItem(newnode.ID, newnode)
#         elif objecttype == 'budgetitem':
#             newnode = BudgetItem(name, desc, 10, 10, context)
#             context.addItem(newnode.ID, newnode)
#         transaction.commit()

#         return HTTPOk()

# @view_config(name = "delete", context=OptimateObject, renderer='json')
# def deleteitemview(context, request):
#     """
#     The deleteitemview is called using the address from the node to be deleted.
#     The node ID is sent in the request, and it is deleted from the context.
#     The try block catches if a node is not found,
#     and returns a 404 http exception
#     """

#     if request.method == 'OPTIONS':
#         return {"success" : True}
#     else:
#         print "context deletion"

#         # Get the parent
#         parent = context.getParent()

#         parent.delete(context.ID)

#         transaction.commit()

#         return HTTPOk()

# @view_config(name = "paste",context=OptimateObject, renderer='json')
# def pasteitemview(context, request):
#     """
#     The pasteitemview is sent the path of the node that is to be copied.
#     That node is then found in the zodb, rebuilt with a new ID and path,
#     and added to the current node.
#     """

#     if request.method == 'OPTIONS':
#         return {"success" : True}
#     else:
#         print "pasting to item"
#         pathlist = request.json_body["Path"][1:-1].split ("/")
#         app_root = appmaker( get_connection(request).root())
#         sourceobject = app_root

#         for pid in pathlist:
#             sourceobject = sourceobject[pid]

#         # need to rebuild target with new id and path
#         # paste = rebuild (sourceobject, context)
#         # context.addItem (paste.ID, paste)
#         context.paste(sourceobject)
#         transaction.commit()

#         return HTTPOk()



