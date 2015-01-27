"""
views.py sets up the view in the web file
it uses json as a renderer
the only response is a data structure containing a hierarchy
of the cost estimate items
"""

from pyramid.view import view_config
from pyramid.response import Response
from models import RootModel, Node, Leaf

@view_config(context=RootModel, renderer='json')
@view_config(context=Node, renderer='json')
@view_config(context=Leaf, renderer='json')
def childview(context, request):
    """
    This view is for when the user requests the children of an item.
     It uses any of the obejcts as it's context, it extracts the subitem (children) from the object,
     adds it to a list and returns it to the JSON renderer
    """

    childrenlist = []
    for key in context.Subitem.keys():
        childrenlist.insert(len(childrenlist), {"Name":context.Subitem[key].Name, "Description":context.Subitem[key].Description,
            "Subitem":[], "ID":context.Subitem[key].ID, "Parent": context.Subitem[key].__parent__})

    return childrenlist
