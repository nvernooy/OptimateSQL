# Models file contains resources used in the project
from persistent import Persistent
from persistent.mapping import PersistentMapping

# The classes used in models only inherit from dict
# The contsructor takes a dictionary of the children, parent id, and name as an id

# The RootModel class is JSON serializable if it is a dict
# If it inherits from PersistantMapping throws TypeError
# class RootModel(PersistentMapping):
#     __name__ = None
#     __parent__ = None

class RootModel(dict):
    __name__ = None
    __parent__ = None

    def __init__(self, children):
        self.projects = children

    def __getitem__ (self, key):
        project = self.projects[key]

        if project != None:
            return project
        else:
            raise KeyError

class Project(dict):
    __parent__ = RootModel

    def __init__(self, children, id):
        self.budgetgroups = children
        self.__name__ = id

    def __getitem__ (self, key):
        budgetgroup = self.budgetgroups[key]

        if budgetgroup != None:
            return budgetgroup
        else:
            raise KeyError


    # def __hash__(self):
    #     """This enables the class to be hashable, it uses the unique ID"""
    #     return self.__name__

    # def __eq__(self, other):
    #     """This enables the class to be hashable, it uses the unique ID"""
    #     return self.__name__ == other.__name__

    def __str__(self):
        """
        The toString method returns a string of the name and
        description of the class.
        If the set is not empty thereafter it prints
        all the BudgetGroups in the set.
        """
        return "Project: " +self.__name__



class BudgetGroup(dict):
    def __init__(self, children, id, parentid):
        self.budgetitems = children
        self.__name__ = id
        self.__parent__ = parentid

    def __getitem__ (self, key):
        budgetitem = self.budgetitems[key]
        if budgetitem!= None:
            return budgetitem
        else:
            raise KeyError

    # def __hash__(self):
    #     """This enables the class to be hashable, it uses the unique ID"""
    #     return self.__name__

    # def __eq__(self, other):
    #     """This enables the class to be hashable, it uses the unique ID"""
    #     return self.__name__ == other.__name__

    def __str__(self):
        """
        The toString method returns a string of the name and
        description of the class.
        If the set is not empty thereafter it prints
        all the BudgetGroups in the set.
        """

        return "BudgetGroup: " +self.__name__



class BudgetItem(dict):

    def __init__(self, id, parent):
        self.__name__ = id
        self.__parent__ = parent

    # def __hash__(self):
    #     """This enables the class to be hashable, it uses the unique ID"""
    #     return self.__name__

    # def __eq__(self, other):
    #     """This enables the class to be hashable, it uses the unique ID"""
    #     return self.__name__ == other.__name__

    def __str__(self):
        """
        The toString method returns a string of the name and
        description of the class.
        If the set is not empty thereafter it prints
        all the BudgetGroups in the set.
        """

        return "BudgetItem: " +self.__name__


# appmakes checks if the root exists in the database
# if not it rebuilds the database.
# Currently the data is hardcoded
def appmaker(zodb_root):
    """appmaker gets the ZODB connection and checks if there is anything in the root.
    If there isn't then the database is built.
    Afterward the root is returned.
    """

    if not 'app_root' in zodb_root:
        budgetitem = BudgetItem("1.1.1", "1.1")
        bidict = {"1.1.1":budgetitem}

        budgetgroup = BudgetGroup(bidict, "1.1", "1")
        bgdict = {"1.1":budgetgroup}

        project = Project(bgdict, "1")
        project2 = Project({}, "2")

        app_root = RootModel({"1":project, "2":project2})

        # project.__parent__ = app_root
        # project2.__parent__ = app_root

        zodb_root['app_root'] = app_root
        import transaction
        transaction.commit()

        # budgetitem = BudgetItem({"Name":"BIName",
        #                                         "Description":"BIDesc",
        #                                         "Quantity":5,
        #                                         "Rate":10,
        #                                          "ID":"1.1.1"
        #                                         })
        # budgetitem.__name__ = budgetitem["ID"]

        # budgetgroup = BudgetGroup({"Name":"BGName",
        #                                             "Description":"BGDesc",
        #                                             "ID":"1.1",
        #                                             "Subitem":budgetitem
        #                                             })
        # budgetgroup.__name__ = budgetgroup["ID"]
        # budgetitem.__parent__ = budgetgroup

        # project = Project({"Name":"PName",
        #                             "Description":"PDesc",
        #                             "ID":"1",
        #                             "Subitem":budgetgroup
        #                             })
        # project.__name__ = project["ID"]
        # budgetgroup.__parent__ = project

        # app_root['Project'] = project
        # project.__parent__ = app_root
        # zodb_root['app_root'] = app_root
        # import transaction
        # transaction.commit()
    return zodb_root['app_root']
