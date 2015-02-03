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

@view_config(name = "add", renderer = 'json')
def additemview(request):
    """
    The postview is called when an http POST request is sent from the client.
    The method find the item that called the POST and adds a child to that parent.
    """
    print "we're in add view"
    print "getting method"
    print request

    if request.method == 'OPTIONS':
        print "options method"
        return {"success" : True}
    else:
        path = request.subpath[0]

        idlist = path.split("/")

        conn = get_connection(request)
        app_root = appmaker(conn.root())

        # If the path only has one id then add to the project
        if len(idlist) == 1:
            print "adding to project"
            bg = BudgetGroup("TestBG", "TestBG Description", idlist[0])
            app_root[idlist[0]].addItem(bg.ID, bg)

        # data = request.json_body

        # print data.items()
        # print (data['Parent'] == '0')
        # conn = get_connection(request)
        # app_root = appmaker(conn.root())

        # # If the Parent ID is 0 then it is a Project item
        # # Follow the path and add a BudgetGroup item
        # if data['Parent'] == '0':
        #     print "adding to project"
        #     bg = BudgetGroup("TestBG", "TestBG Description", data['ID'])
        #     app_root[data['ID']].addItem(bg.ID, bg)

        # # If the Parent ID is not 0 then it is a BudgetGroup item
        # # Follow the path and add a BudgetItem item
        # else:
        #     print  "adding to budgetgroup"
        #     bi = BudgetItem("TestBI", "TestBI Description", data['ID'])
        #     app_root[data['Parent']][data['ID']].addItem(bi.ID, bi)

        # print "commiting transaction"
        conn.root()['app_root'] = app_root
        import transaction
        transaction.commit()

        print "returning success"
        return {"success" : True}
