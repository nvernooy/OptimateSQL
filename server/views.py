"""
views.py sets up the view in the web file
it uses json as a renderer
the only response is a data structure containing a hierarchy
of the cost estimate items
"""

from pyramid.view import view_config
from models import Project, BudgetGroup, BudgetItem


class DataViews:
    """Class acts as a mediator between data and the output thereof.

    Method convertdata() gets a list and transforms it into a list
    of dictionaries for use by the JSON renderer. """

    def __init__(self, request):
        """init method to make the class into a module"""
        self.request = request

    @view_config(route_name='Data', renderer='json')
    def formatdata(self):
        """The method gets a list of the data structures and transforms
        it into a format usable by JSON.

        The list comes from filedata and is formatted into a list of
        dictionaries, the result is returned."""

        # Get the list from the filedata() method and declare an empty list.
        projectlist = self.filedata()
        JSONlist = []

        # Iterate through the list and convert the data into dictionaries.
        for project in projectlist:
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
        return JSONlist

    def filedata(self):
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


"""if __name__ == "__main__":
    print DataViews(None).formatdata()"""
