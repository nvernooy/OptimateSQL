from models import Project, BudgetGroup, BudgetItem
import transaction
from ZODB import FileStorage, DB
#from BTrees.OOBTree import OOBTree


class ZODBcontrol():
    """
    Class ZODBcontrol manages the reading and writing of the database.
    It returns the data as a list of the projects.
    """

    def __init__(self):
        """
        Instantiating the object creates a connection to the database.
        """
        self.storage = FileStorage.FileStorage('ProjectData.fs')
        self.db = DB(self.storage)
        self.connection = self.db.open()
        self.projectDB = self.connection.root()

    def close(self):
        """
        Closes the connection to the database.
        """
        self.connection.close()
        self.db.close()
        self.storage.close()

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

    def databasedata(self):
        """The method creates a connection with ZODB and manages the project
        data that is in it.
        It adds project data to the database if it is not there, otherwise
        it prints out all the data in the database.
        """

        # If the projects table does not exist in the database, create it.
        if len(self.projectDB.keys()) == 0:
            #projectDB = OOBTree()

            # Run the filedData method that returns a list of projects
            projectdatalist = self.filedata()

            # Add the Project list to the database,
            # using the Project ID as the key.
            for project in projectdatalist:
                self.projectDB[project.ID] = project

            transaction.commit()

        # Get a list of the items in the database
        datalist = []
        for key in self.projectDB.keys():
            datalist.insert(len(datalist), self.projectDB[key])

        # Return the list
        return datalist

    def getProject(self, projectID):
        """Returns a Project specified by the ID"""

        project = self.projectDB[projectID]

        return project

#if __name__ == "__main__":
    #zodb = ZODBcontrol()
    #zodb.databasedata()
    #print zodb.getProject("6b3df58c9c9811e49239000c29a3e37c")


class RootModel(PersistentMapping):
    __parent__ = __name__ = None

def appmaker(zodb_root):
    if not 'db_root' in zodb_root:
        db_root = RootModel()
        zodb_root['db_root'] = db_root
        import transaction
        transaction.commit()
    return zodb_root['db_root']
