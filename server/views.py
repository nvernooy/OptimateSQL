"""
views uses pyramid and sqlalchemy to recieve requests from a user
and send responses with appropriate data
"""

import uuid
import transaction
from pyramid.view import view_config

from pyramid.httpexceptions import (
    HTTPOk,
    HTTPFound,
    HTTPNotFound,
    HTTPInternalServerError,
    )

from .models import (
    DBSession,
    Node,
    Project,
    BudgetGroup,
    BudgetItem,
    )


@view_config(route_name='rootview', renderer='json')
@view_config(route_name="childview", renderer='json')
def childview(request):
    """
    This view is for when the user requests the children of an item.
    The parent's id is derived from the path of the request,
    or if there is no id in the path the root id '0' is assumed.
    It extracts the children from the object,
    adds it to a list and returns it to the JSON renderer
    """

    parentid = '0'
    if 'parentid' in request.matchdict:
        parentid = request.matchdict['parentid']

    print "\n\n\nIn Child view: "+ parentid+"\n\n"
    childrenlist = []

    # Execute the sql query on the Node table to find all objects with that parent
    qry = DBSession.query(Node).filter_by(ParentID=parentid).all()

    # Format the result into a json readable list and respond with that
    for value in qry:
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
        # Get the parent to add the object to from the path
        parentid = request.matchdict['id']
        print "adding to item: " + str(parentid)

        # Get the data to be added to the new object from the request body
        name = request.json_body['Name']
        desc = request.json_body['Description']
        objecttype = request.json_body['Type']

        # Check if it is so be added to the root or not
        if parentid != '0':
            # Find the parent by going through the object tables
            parent = DBSession.query(Project).filter_by(ID=parentid).first()
            if parent == None:
                parent = DBSession.query(BudgetGroup).filter_by(ID=parentid).first()
                if parent == None:
                    parent = DBSession.query(BudgetItem).filter_by(ID=parentid).first()
                    if parent == None:
                        return HTTPNotFound()

            # Determine the type of object to be added and build it and append it
            if objecttype == 'project':
                parent.Children.append(Project(Name=name,
                                                Description=desc,
                                                ParentID=parentid))
            elif objecttype == 'budgetgroup':
                parent.Children.append(BudgetGroup(Name=name,
                                                    Description=desc,
                                                    ParentID=parentid))
            elif objecttype == 'budgetitem':
                parent.Children.append(BudgetItem(Name=name,
                                                    Description=desc,
                                                    ParentID=parentid,
                                                    Quantity=10,
                                                    Rate=5))
            else:
                return HTTPInternalServerError()
        # if it is to be added to the root it does not have a parent
        else:
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
    The node ID is sent in the request, and it is deleted from the tables.
    """

    if request.method == 'OPTIONS':
        return {"success" : True}
    else:
        # Get the id of the node to be deleted from the path
        deleteid = request.matchdict['id']
        print "\n\nDeleting node: " + str(deleteid) +"\n\n"

        # Deleting it from the node table deleted the object
        qry = DBSession.query(Node).filter_by(ID=deleteid).delete(
                    synchronize_session='fetch')
        if qry == 0:
            return HTTPNotFound()

        transaction.commit()

        return HTTPOk()

@view_config(route_name = "pasteview", renderer='json')
def pasteitemview(request):
    """
    The pasteitemview is sent the path of the node that is to be copied.
    That node is then found in the db, copied with the new parent's id,
    and added to the current node.
    """

    if request.method == 'OPTIONS':
        return {"success" : True}
    else:
        print "pasting to item"
        # Find the source object to be copied from the path in the request body
        sourceid = request.json_body["Path"][1:-1]
        # Find the object to be copied to from the path
        destinationid = request.matchdict['id']

        # Find the source object in the tables
        source= DBSession.query(Project).filter_by(ID=sourceid).first()
        if source == None:
            source = DBSession.query(BudgetGroup).filter_by(ID=sourceid).first()
            if source == None:
                source = DBSession.query(BudgetItem).filter_by(ID=sourceid).first()
                if source == None:
                    return HTTPNotFound()

        # Find the destination object in the tables
        dest= DBSession.query(Project).filter_by(ID=destinationid).first()
        if dest == None:
            dest = DBSession.query(BudgetGroup).filter_by(ID=destinationid).first()
            if dest == None:
                dest = DBSession.query(BudgetItem).filter_by(ID=destinationid).first()
                if dest == None:
                    return HTTPNotFound()

        # Paste the source into the destination
        dest.paste(source.copy(dest.ID), source.Children)

        return HTTPOk()
