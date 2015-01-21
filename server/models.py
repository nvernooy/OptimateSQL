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

    def __init__(self, children, nam, desc):
        self.budgetgroups = children
        self.Name = nam
        self.Description = desc
        self.ID = "1"
        self.__name__ = self.ID

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

    # def __str__(self):
    #     """
    #     The toString method returns a string of the name and
    #     description of the class.
    #     If the set is not empty thereafter it prints
    #     all the BudgetGroups in the set.
    #     """
    #     return "Project: " +self.__name__



class BudgetGroup(dict):
    def __init__(self, children, nam, desc, parentid):
        self.budgetitems = children
        self.Name = nam
        self.Description = desc
        self.ID = "1.1"
        self.__name__ = self.ID
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

    # def __str__(self):
    #     """
    #     The toString method returns a string of the name and
    #     description of the class.
    #     If the set is not empty thereafter it prints
    #     all the BudgetGroups in the set.
    #     """

    #     return "BudgetGroup: " +self.__name__



class BudgetItem(dict):

    def __init__(self, nam, desc, quan, rate, parentid):
        self.Name = nam
        self.Description = desc
        self.Quantity = quan
        self.Rate = rate
        self.ID = "1.1.1"
        self.__name__ = self.ID
        self.__parent__ = parentid

    # def __hash__(self):
    #     """This enables the class to be hashable, it uses the unique ID"""
    #     return self.__name__

    # def __eq__(self, other):
    #     """This enables the class to be hashable, it uses the unique ID"""
    #     return self.__name__ == other.__name__

    # def __str__(self):
    #     """
    #     The toString method returns a string of the name and
    #     description of the class.
    #     If the set is not empty thereafter it prints
    #     all the BudgetGroups in the set.
    #     """

    #     return "BudgetItem: " +self.__name__


# appmakes checks if the root exists in the database
# if not it rebuilds the database.
# Currently the data is hardcoded
def appmaker(zodb_root):
    """appmaker gets the ZODB connection and checks if there is anything in the root.
    If there isn't then the database is built.
    Afterward the root is returned.
    """

    if not 'app_root' in zodb_root:
        print "building the db again"
        budgetitem = BudgetItem("BIName", "BIDesc", 10, 5, "1.1")
        bidict = {budgetitem.ID:budgetitem}

        budgetgroup = BudgetGroup(bidict, "BGName", "BGDesc", "1")
        bgdict = {budgetgroup.ID:budgetgroup}

        project = Project(bgdict, "PName", "PDesc")

        app_root = RootModel({project.ID:project})

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
