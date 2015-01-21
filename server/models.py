# Models file contains resources used in the project
from persistent import Persistent
from persistent.mapping import PersistentMapping

# The classes used in models only inherit from dict and have no attributes or methods yet
class RootModel(PersistentMapping):
    __name__ = None
    __parent__ = None

class Project(dict):
    def __init__(self, a_dict):
        super(Project, self).__init__(self)
        self.update(a_dict)
        self.__name__ = None
        self.__parent__ = None

class BudgetGroup(dict):
    def __init__(self, a_dict):
        super(BudgetGroup, self).__init__(self)
        self.update(a_dict)
        self.__name__ = None
        self.__parent__ = None

class BudgetItem(dict):
    def __init__(self, a_dict):
        super(BudgetItem, self).__init__(self)
        self.update(a_dict)
        self.__name__ = None
        self.__parent__ = None


# appmakes checks if the root exists in the database
# if not it rebuilds the database.
# Currently the data is hardcoded
def appmaker(zodb_root):
    if not 'app_root' in zodb_root:

        app_root = RootModel()

        budgetitem = BudgetItem({"Name":"BIName",
                                                "Description":"BIDesc",
                                                "Quantity":5,
                                                "Rate":10,
                                                 "ID":"1.1.1"
                                                })
        budgetitem.__name__ = budgetitem["ID"]

        budgetgroup = BudgetGroup({"Name":"BGName",
                                                    "Description":"BGDesc",
                                                    "ID":"1.1",
                                                    "Subitem":budgetitem
                                                    })
        budgetgroup.__name__ = budgetgroup["ID"]
        budgetitem.__parent__ = budgetgroup                        

        project = Project({"Name":"PName",
                                    "Description":"PDesc",
                                    "ID":"1",
                                    "Subitem":budgetgroup
                                    })
        project.__name__ = project["ID"]
        budgetgroup.__parent__ = project                       

        app_root['Project'] = project
        project.__parent__ = app_root
        zodb_root['app_root'] = app_root
        import transaction
        transaction.commit()
    return zodb_root['app_root']
