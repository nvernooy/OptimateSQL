from models import Project, BudgetGroup, BudgetItem
import transaction
import ZODB
import ZODB.FileStorage
from BTrees.OOBTree import OOBTree


def filedata():
    """
    Add data to the database using a file on the system.

    The file is preformatted to enable the method to parse
    and build the relevant data structures.
    """

    projectlist = []
    try:
        # Open the data file and read the first line.
        datafile = open("data.txt", "r")
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
    print projectDB.items()
    projects =
    print projectDB.projects

    datalist = []
    # If the projects table does not exist in the database, create it.
    # Test if the table exist by referencing it:
    try:
        # Try and get the size of the table.
        # If it does not exist an exception will be raised
        # and a new table built
        len(projectDB.projects)
    except:
        projectDB.projects = OOBTree()

        # Run the addData method that returns a finished Project
        projectdatalist = filedata()

        # Add the Project list to the database,
        # using the Project ID as the key.
        for project in projectdatalist:
            projectDB.projects[project.ID] = project
            # Commit the change to the database
            transaction.commit()

    for key in projectDB.projects.keys():
            datalist.insert(len(datalist), projectDB.projects[key])

    #pdb.set_trace()
    # Close the database
    connection.close()
    db.close()
    storage.close()

    # Return the list
    return datalist


if __name__ == "__main__":
    tmplist = databasedata()
    for project in tmplist:
        print project