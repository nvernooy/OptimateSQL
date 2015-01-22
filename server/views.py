"""
views.py sets up the view in the web file
it uses json as a renderer
the only response is a data structure containing a hierarchy
of the cost estimate items
"""

from pyramid.view import view_config
from pyramid.response import Response
from models import RootModel, Project, BudgetGroup, BudgetItem


# This view is for when the RootModel is the context
# It formats the project information in RootModel to be usable by angular treeview
# So far it only returns a list of the projectids no further information about the projects
@view_config(context=RootModel, renderer='json')
def rootview(context, request):
    # get the projects from the context
    data = context.__dict__

    # for item in data.items():
    #     print item

    childrenlist = []
    for key in data["projects"].keys():
        childrenlist.insert(len(childrenlist), {"Name":key, "Description":key, "Subitem":[], "ID":key, "Parent": "0"})

    for item in childrenlist:
        print item
    #projects = data["data"]["Project"]
    # JSON expects the data to be a dictionary in a list
    #JSONlist = [data]
    #return JSONlist
    return childrenlist

# @view_config(route_name = 'children', context=RootModel, renderer='json')
# def rootview(context, request):
#     # get the projects from the context
#     data = context.__dict__

#     for item in data.items():
#         print item

#     childrenlist = []
#     for key in data["projects"].keys():
#         childrenlist.insert(len(childrenlist), {"Name":key, "Description":key, "Subitem":[], "ID":key})


#     #projects = data["data"]["Project"]
#     # JSON expects the data to be a dictionary in a list
#     #JSONlist = [data]
#     return childrenlist


@view_config(context=Project, renderer='json')
def projectview(context, request):
    # get the projects from the context
    data = context.__dict__

    # for item in data.items():
    #     print item

    childrenlist = []
    for key in data["budgetgroups"].keys():
        childrenlist.insert(len(childrenlist), {"Name":key, "Description":key, "Subitem":[], "ID":key, "Parent": data["ID"]})

    for item in childrenlist:
        print item

    #projects = data["data"]["Project"]
    # JSON expects the data to be a dictionary in a list
    #JSONlist = [data]
    return childrenlist


@view_config(context=BudgetGroup, renderer='json')
def budgetgroupview(context, request):
    # get the projects from the context
    data = context.__dict__

    # for item in data.items():
    #     print item

    childrenlist = []
    for key in data["budgetitems"].keys():
        childrenlist.insert(len(childrenlist), {"Name":key, "Description":key, "Subitem":[], "ID":key, "Parent": data["ID"]})

    for item in childrenlist:
        print item

    #projects = data["data"]["Project"]
    # JSON expects the data to be a dictionary in a list
    #JSONlist = [data]
    return childrenlist

@view_config(context=BudgetItem, renderer='json')
def budgetitemview(context, request):
    # get the projects from the context
    data = context.__dict__

    # for item in data.items():
    #     print item

    childrenlist = [{"Parent": data["ID]"]}]

    for item in childrenlist:
        print item

    #projects = data["data"]["Project"]
    # JSON expects the data to be a dictionary in a list
    #JSONlist = [data]
    return childrenlist

# Return all the data
# The context is dependant on the object returned on the traversal
# Only the content of the object, as a dict, is in the response
# @view_config(context=RootModel, renderer='json')
# @view_config(context=Project, renderer='json')
# @view_config(context=BudgetGroup, renderer='json')
# @view_config(context=BudgetItem, renderer='json')
# def traversalview(context, request):
#     # get the projects from the context
#     data = context.__dict__

#     #projects = data["data"]["Project"]
#     # JSON expects the data to be a dictionary in a list
#     JSONlist = [data]
#     return JSONlist


# Traverse to the projects
# @view_config(context=Project, renderer='json')
# def traversalview(context, request):
#     # get the projects from the context
#     data = context.__dict__
#     # print data.keys()
#     # for keys in data.items():
#     #     print keys

#     budgetitems = [data["__parent__"]["Project"]["Subitem"]["Subitem"]]
#     budgetgroup = [data["__parent__"]["Project"]["Subitem"]]
#     project = [data["__parent__"]["Project"]]

#     for item in budgetitems:
#         print item

#     datalist = [project.insert(0, budgetgroup.insert(0, budgetitems))]

#     #projects = data["data"]["Project"]
#     # JSON expects the data to be a dictionary in a list
#     JSONlist = [data]
#     return project

# Return all the projects
# @view_config(context='.models.RootModel.data.Project', renderer='json')
# def traversalview(context, request):
#     # get the projects from the context
#     data = context.__dict__
#     # projects = data["data"]["Project"]
#     # JSON expects the data to be a dictionary in a list
#     JSONlist = [data]
#     return JSONlist
