"""
views.py sets up the view in the web file
it uses json as a renderer
the only response is a data structure containing a hierarchy
of the cost estimate items
"""

from pyramid.view import view_config
import zodbcontrol


@view_config(route_name='data', renderer='json')
def formatdata(request):
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
    preformatlist = zodbcontrol.databasedata()
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
            budgetgrouplist.insert(len(budgetitemlist),
                {"Name": budgetgroup.Name,
                "Description": budgetgroup.Description,
                "Subitem": budgetitemlist,
                "ID": budgetgroup.ID})

        JSONlist.insert(len(budgetitemlist),
            {"Name": project.Name,
            "Description": project.Description,
            "Subitem": budgetgrouplist,
            "ID": project.ID})

    # Return the finished list of projects, groups, and items.
    #pdb.set_trace()
    return JSONlist