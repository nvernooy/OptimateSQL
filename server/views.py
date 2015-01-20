"""
views.py sets up the view in the web file
it uses json as a renderer
the only response is a data structure containing a hierarchy
of the cost estimate items
"""

from pyramid.view import view_config
from zodbcontrol import ZODBcontrol


@view_config(route_name='all_data', renderer='json')
def all_data(request):
    """The method gets a list of the data structures and transforms
    it into a format usable by JSON.

    The list comes from databasedata() and is formatted into a list of
    dictionaries, the result is returned."""

    # Add CORS headers to the response
    response = request.response

    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Content-Type"] = "application/json"
    response.headers["Access-Control-Allow-Headers"] =     \
                    "Origin, X-Requested-With, Content-Type, Accept"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, PUT, DELETE"

    # Get the list from the filedata() method and declare an empty list.
    db = ZODBcontrol()
    preformatlist = db.databasedata()
    #preformatlist = zodbcontrol.filedata()

    JSONlist = []
    # Iterate through the list and convert the data into dictionaries.
    for project in preformatlist:
        budgetgrouplist = []

        for budgetgroup in project.GroupSet:
            budgetitemlist = []

            for budgetitem in budgetgroup.ItemSet:
                budgetitemlist.insert(len(budgetitemlist),
                    {"Name": budgetitem.Name,
                    "Description": budgetitem.Description,
                    "Quantity": budgetitem.Quantity,
                    "Rate": budgetitem.Rate,
                    "ID": budgetitem.ID,
                    "Subitem": []})

            # Build each list and then add it to the dictionary
            budgetgrouplist.insert(len(budgetgrouplist),
                {"Name": budgetgroup.Name,
                "Description": budgetgroup.Description,
                "Subitem": budgetitemlist,
                "ID": budgetgroup.ID})

        JSONlist.insert(len(JSONlist),
            {"Name": project.Name,
            "Description": project.Description,
            "Subitem": budgetgrouplist,
            "ID": project.ID})

    # Return the finished list of projects, groups, and items.
    #pdb.set_trace()
    db.close()
    return JSONlist


@view_config(route_name='projects', renderer='json')
def projects(request):
    """The method gets a list of the data structures and returns a list
    of only the Projects in a JSON structure.

    The list comes from databasedata() and is formatted into a list of
    dictionaries, the result is returned."""

    # Add CORS headers to the response
    response = request.response

    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Content-Type"] = "application/json"
    response.headers["Access-Control-Allow-Headers"] =     \
                    "Origin, X-Requested-With, Content-Type, Accept"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, PUT, DELETE, OPTIONS"
    print request.method
    # Get the header containing the id for the item requested
    currentid = request.headers['id']

    db = ZODBcontrol()
    JSONlist = []
    # # If the id is 0 then it is the root projects requested
    # if currentid == "0":
    #     # Get the list from the filedata() method
    #     preformatlist = db.databasedata()
    #     #preformatlist = zodbcontrol.filedata()

    #     # Iterate through the list and get the Projects.
    #     for project in preformatlist:
    #         # Add only the Project data to the list
    #         JSONlist.insert(len(JSONlist),
    #             {"Name": project.Name,
    #             "Description": project.Description,
    #             "Subitem": [],
    #             "ID": project.ID})
    # # If the id is not 0 get the next level of items
    # elif currentid != "0":
    #     specified_project = db.getProject(currentid)

    #     # Iterate through the Project and get all the data.
    #     budgetgrouplist = []

    #     for budgetgroup in specified_project.GroupSet:
    #         # Build each list and then add it to the dictionary
    #         budgetgrouplist.insert(len(budgetgrouplist),
    #             {"Name": budgetgroup.Name,
    #             "Description": budgetgroup.Description,
    #             "Subitem": [],
    #             "ID": budgetgroup.ID})

    #     JSONlist.insert(len(JSONlist),
    #         {"Name": specified_project.Name,
    #         "Description": specified_project.Description,
    #         "Subitem": budgetgrouplist,
    #         "ID": specified_project.ID})

    # # Return the finished list of projects, groups, and items.
    # db.close()
    return JSONlist


@view_config(route_name='projectdata', renderer='json')
def project_data(request):
    """The method gets a list of the data structures and returns only the
    information of a specified Project

    The list comes from databasedata() and the specified Project is extracted
    from it, the result is returned."""

    # Add CORS headers to the response
    response = request.response

    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Content-Type"] = "application/json"
    response.headers["Access-Control-Allow-Headers"] =     \
                    "Origin, X-Requested-With, Content-Type, Accept"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, PUT, DELETE"

    # Get the project ID from the header
    projectID = request.headers['id']
    #projectID = request.query_string()

    # # Get the list from the filedata() method and declare an empty list.
    # db = ZODBcontrol()
    # specified_project = db.getProject(projectID)
    # #preformatlist = zodbcontrol.filedata()

    # JSONlist = []
    # # Iterate through the Project and get all the data.
    # budgetgrouplist = []

    # for budgetgroup in specified_project.GroupSet:
    #     # Build each list and then add it to the dictionary
    #     budgetgrouplist.insert(len(budgetgrouplist),
    #         {"Name": budgetgroup.Name,
    #         "Description": budgetgroup.Description,
    #         "Subitem": [],
    #         "ID": budgetgroup.ID})

    # JSONlist.insert(len(JSONlist),
    #     {"Name": specified_project.Name,
    #     "Description": specified_project.Description,
    #     "Subitem": budgetgrouplist,
    #     "ID": specified_project.ID})

    # # Return the finished list of projects, groups, and items.
    # #pdb.set_trace()
    # print JSONlist
    # db.close()
    return {"id": projectID}


#if __name__ == "__main__":
        #tmplist = project_data(None)
        #print len(tmplist)
        #print tmplist[0]
