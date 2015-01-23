# Models file contains resources used in the project
from persistent import Persistent
from persistent.mapping import PersistentMapping
from BTrees.OOBTree import OOSet
import uuid

# The classes used in models only inherit from dict
# The contsructor takes a dictionary of the children, parent id, and name as an id

# The RootModel class is JSON serializable if it is a dict
# If it inherits from PersistantMapping throws TypeError
# class RootModel(PersistentMapping):
#     __name__ = None
#     __parent__ = None

class RootModel(PersistentMapping):
    __name__ = None
    __parent__ = None

    def __init__(self, children = OOSet()):
        self.Subitem = children
        self.ID = "0"

    def addSet (self, children):
        self.Subitem = children

    def __getitem__ (self, key):
        child = self.Subitem[key]

        if child != None:
            return child
        else:
            raise KeyError

class Project(PersistentMapping):
    __parent__ = "0"

    def __init__(self, nam, desc, children = OOSet()):
        self.budgetgroups = children
        self.Name = nam
        self.Description = desc
        self.ID = uuid.uuid1().hex    # The ID is the hex value of a UUID
        self.__name__ = self.ID

    def addSet (self, children):
        self.Subitem = children

    def __getitem__ (self, key):
        child = self.Subitem[key]

        if child != None:
            return child
        else:
            raise KeyError


class BudgetGroup(PersistentMapping):
    def __init__(self, nam, desc, parentid, children = OOSet()):
        self.Subitem = children
        self.Name = nam
        self.Description = desc
        self.ID = uuid.uuid1().hex    # The ID is the hex value of a UUID
        self.__name__ = self.ID
        self.__parent__ = parentid

    def addSet (self, children):
        self.Subitem = children

    def __getitem__ (self, key):
        child = self.Subitem[key]

        if child != None:
            return child
        else:
            raise KeyError


class BudgetItem(PersistentMapping):

    def __init__(self, nam, desc, quan, rate, parentid):
        self.Name = nam
        self.Description = desc
        self.Quantity = quan
        self.Rate = rate
        self.ID = uuid.uuid1().hex    # The ID is the hex value of a UUID
        self.__name__ = self.ID
        self.__parent__ = parentid


def appmaker(zodb_root):
    """appmaker gets the ZODB connection and checks if there is anything in the root.
    If there isn't then the database is built.
    Afterward the root is returned.
    """

    if not 'app_root' in zodb_root:

        # Build the Projects
        project = Project("PName", "PDesc")

        # Build the next level in the hierarchy
        budgetgroup = BudgetGroup("BGName", "BGDesc", project.ID)

        # Build the next level
        budgetitem = BudgetItem("BIName", "BIDesc", 10, 5, budgetgroup.ID)

        # Build the hierarchy
        budgetgroup.addSet({budgetitem.ID:budgetitem})
        project.addSet({budgetgroup.ID:budgetgroup})
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
