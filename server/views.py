import cgi
import re
from docutils.core import publish_parts

from pyramid.httpexceptions import (
    HTTPOk,
    HTTPFound,
    HTTPNotFound,
    HTTPInternalServerError,
    )
from pyramid.view import view_config

from .models import (
    DBSession,
    Root,
    Project,
    BudgetGroup,
    BudgetItem,
    )

from sqlalchemy import *
from sqlalchemy.orm import *

import uuid


@view_config(route_name= 'root', renderer='json')
def rootview(request):
    """
    This view acts as the root of the server.
    It finds all the models that have the root as its parent,
    adds it to a list and returns it to the JSON renderer
    """
    print "\n\n\nIn Root view\n\n"
    childrenlist = []

    querylist = [DBSession.query(Project).filter_by(ParentID="0").all(),
                DBSession.query(BudgetGroup).filter_by(ParentID="0").all(),
                DBSession.query(BudgetItem).filter_by(ParentID="0").all()]

    for query in querylist:
        for value in query:
            childrenlist.insert(len(childrenlist), {
                "Name":value.Name,
                "Description":value.Description,
                "Subitem":[],
                "ID":value.ID,
                "Path": "/" +  str(value.ID)+"/"})


    return childrenlist


@view_config(route_name="childview", renderer='json')
def childview(request):
    """
    This view is for when the user requests the children of an item.
    It uses any of the obejcts as it's context,
    it extracts the subitem (children) from the object,
    adds it to a list and returns it to the JSON renderer
    """

    parentid = request.matchdict['parentid']
    print "\n\n\nIn Child view: "+ parentid+"\n\n"
    childrenlist = []

    querylist = [DBSession.query(Project).filter_by(ParentID=parentid).all(),
                DBSession.query(BudgetGroup).filter_by(ParentID=parentid).all(),
                DBSession.query(BudgetItem).filter_by(ParentID=parentid).all()]

    for query in querylist:
        for value in query:
            childrenlist.insert(len(childrenlist), {
                "Name":value.Name,
                "Description":value.Description,
                "Subitem":[],
                "ID":value.ID,
                "Path": "/" + str(value.ID)+"/"})

    return childrenlist



@view_config(route_name="addview", renderer='json')
def additemview(request):
    """
    The additemview is called when an http POST request is sent from the client.
    The method adds a new node with attributes as specified by the user
    to the current node.
    """

    if request.method == 'OPTIONS':
        return {"success" : True}
    else:
        parentid = request.matchdict['id']
        print "adding to item: " + str(parentid)

        name = request.json_body['Name']
        desc = request.json_body['Description']
        objecttype = request.json_body['Type']

        if objecttype == 'project':
            newnode = Project(Name=name,Description=desc,ParentID=parentid)
            DBSession.add(newnode)
        elif objecttype == 'budgetgroup':
            newnode = BudgetGroup(Name=name,Description=desc,ParentID=parentid)
            DBSession.add(newnode)
        elif objecttype == 'budgetitem':
            newnode = BudgetItem(Name=name,Description=desc,ParentID=parentid, Quantity=10, Rate=5)
            DBSession.add(newnode)
        else:
            return HTTPInternalServerError()

        return HTTPOk()

@view_config(route_name = "deleteview",renderer='json')
def deleteitemview(request):
    """
    The deleteitemview is called using the address from the node to be deleted.
    The node ID is sent in the request, and it is deleted from the context.
    """

    if request.method == 'OPTIONS':
        return {"success" : True}
    else:
        print "context deletion"
        deleteid = request.matchdict['id']

        DBSession.query(Project).filter_by(ID=deleteid).delete()
        DBSession.query(BudgetGroup).filter_by(ID=deleteid).delete()
        DBSession.query(BudgetItem).filter_by(ID=deleteid).delete()

        return HTTPOk()

@view_config(route_name = "pasteview", renderer='json')
def pasteitemview(request):
    """
    The pasteitemview is sent the path of the node that is to be copied.
    That node is then found in the zodb, rebuilt with a new ID and path,
    and added to the current node.
    """

    if request.method == 'OPTIONS':
        return {"success" : True}
    else:
        print "pasting to item"
        sourceid = request.json_body["Path"][1:-1]
        print sourceid

        destinationid = request.matchdict['id']

        source= DBSession.query(Project).filter_by(ID=sourceid).first()
        if source == None:
            source = DBSession.query(BudgetGroup).filter_by(ID=sourceid).first()
        if source == None:
            source = DBSession.query(BudgetItem).filter_by(ID=sourceid).first()

        print "\n\nPrinting source children:"
        for item in source.Children:
            print "ID: "+ item.ID

        print "\n\n"

        dest= DBSession.query(Project).filter_by(ID=destinationid).first()
        if dest == None:
            dest = DBSession.query(BudgetGroup).filter_by(ID=destinationid).first()
        if dest == None:
            dest = DBSession.query(BudgetItem).filter_by(ID=destinationid).first()

        dest.paste(source.copy(dest.ID), source.Children)

        # DBSession.add(copied)

        return HTTPOk()
