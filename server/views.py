"""
views.py sets up the view in the web file
it uses json as a renderer
the only response is a data structure containing a hierarchy
of the cost estimate items
"""

from pyramid.view import view_config
from models import Project, BudgetGroup, BudgetItem
import ZODB
import ZODB.FileStorage
import transaction
from BTrees.OOBTree import OOBTree


@view_config(route_name='Data', renderer='json')
def formatdata(request):
    """The method gets a list of the data structures and transforms
    it into a format usable by JSON.

    The list comes from databasedata() and is formatted into a list of
    dictionaries, the result is returned."""

    # Do the CORS thingie
    response = request.response

    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Content-Type"] = "application/json"
    response.headers["Access-Control-Allow-Headers"] =     \
                    "Origin, X-Requested-With, Content-Type, Accept"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, PUT, DELETE"

    # Get the list from the filedata() method and declare an empty list.
    preformatlist = databasedata()
    #preformatlist = filedata()
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
                    "Rate": budgetitem.Rate})

            # Build each list and then add it to the dictionary
            budgetgrouplist.insert(len(budgetitemlist),
                {"Name": budgetgroup.Name,
                "Description": budgetgroup.Description,
                "BudgetItems": budgetitemlist})

        JSONlist.insert(len(budgetitemlist),
            {"Name": project.Name,
            "Description": project.Description,
            "BudgetGroup": budgetgrouplist})

    # Return the finished list of projects, groups, and items.
    #return JSONlist

    return [{"Name":"A", "Description":"desc"}]


def filedata():
    """
    Add data to the database using a file on the system.

    The file is preformatted to enable the method to parse
    and build the relevant data structures.
    """

    projectlist = []
    try:
        # Open the data file and read the first line.
        datafile = open("simpledata.txt", "r")
        line = datafile.next().rstrip()

        # Iterate until the End Of File is reached.
        while line != "EOF":

            # "=" indicates the following is a Project structure
            if line == "=":
                # Read the data and initialise the Project.
                name = datafile.next().rstrip()
                desc = datafile.next().rstrip()
                project = Project(name, desc)

                line = datafile.next().rstrip()
                while line != "=" and line != "EOF":
                    # "+" indicates a BudgetGroup
                    if line == "+":
                        gname = datafile.next().rstrip()
                        gdesc = datafile.next().rstrip()
                        budgetgroup = BudgetGroup(gname, gdesc)
                        line = datafile.next().rstrip()

                        while line != "+" and line != "=":
                            # "*" indicates a BudgetItem
                            if line == "*":
                                iname = datafile.next().rstrip()
                                idesc = datafile.next().rstrip()
                                iquantity = float(datafile.next().rstrip())
                                irate = float(datafile.next().rstrip())

                                budgetitem = BudgetItem(iname, idesc,
                                                iquantity, irate)

                                # Add the items to the BudgetGroup list.
                                budgetgroup.add(budgetitem)
                                line = datafile.next().rstrip()

                            # If the EOF is reached stop the iteration
                            if line == "EOF":
                                break
                        # Add the BudgetGroup list to the Project list
                        project.add(budgetgroup)

                projectlist.insert(len(projectlist), project)
        datafile.close()
    except:
        pass

    # Return the complete list of data structures
    return projectlist


def databasedata():
    """The method creates a connection with ZODB and manages the project
    data that is in it.

    It adds project data to the database if it is not there, otherwise
    it prints out all the data in the database.
    """

    # Create the database connection.
    storage = ZODB.FileStorage.FileStorage('ProjectData.fs')
    db = ZODB.DB(storage)
    connection = db.open()
    projectDB = connection.root()

    # If the projects table does not exist in the database, create it.
    if len(projectDB) == 0:
        projectDB.projects = OOBTree()

        # Run the addData method that returns a finished Project
        projectdatalist = filedata()

        # Add the Project list to the database,
        # using the Project ID as the key.
        for project in projectdatalist:
            projectDB.projects[project.ID] = project
            # Commit the change to the database
            transaction.commit()

    # Get a list of the items in the database
    datalist = []
    for key in projectDB.projects.keys():
        datalist.insert(len(datalist), projectDB.projects[key])

    # Close the database
    transaction.commit()
    connection.close()
    db.close()
    storage.close()

    # Return the list
    return datalist

#if __name__ == "__main__":
    #tmplist = formatdata(None)
    #for project in tmplist:
        #print project
