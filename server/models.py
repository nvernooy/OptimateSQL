# Models file contains resources used in the project
# from persistent import Persistent
# from BTrees.OOBTree import OOBTree
# import uuid
# import os.path
# import copy
# import sys

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    )

from pyramid.security import (
    Allow,
    Everyone,
    )


from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

# class OptimateObject (Base):
#     """
#     The base class of the Optimate project classes
#     It inherits from Persistent, and implements the __getitem__ method
#     """

#     __tablename__ = 'models'
#     ID = Column(Integer, primary_key=True)
#     Name = Column(Text)
#     Description = Column(Text)
#     Path = Column(Text)

# class OptimateObject (Persistent):
#     """
#     The base class of the Optimate project classes
#     It inherits from Persistent, and implements the __getitem__ method
#     """

#     def __init__(self, name, desc, parent):
#         self.__parent__ = parent
#         self.Name = name
#         self.Description = desc
#         self.ID = uuid.uuid1().hex
#         self.__name__ = self.ID
#         self.Subitem = OOBTree()
#         self.Path = ""

#     def addSet(self, children):
#         """
#         Gets a set of children from it's parameter and adds it to the Subitem
#         """

#         self.Subitem = children

#     def addItem (self, key, item):
#         """
#         Gets a new item and adds it to the Subitem set.
#         The item's path is rebuilt.
#         """

#         item.addPath (self.Path)
#         self.Subitem.insert (key, item)

#     def items(self):
#         """
#         Returns a list of the items in the Subitem set.
#         """

#         return self.Subitem.items()

#     def delete (self, key):
#         """
#         Deletes the child from the object using it's key.
#         """

#         del self.Subitem[key]

#     def addPath (self, path):
#         """
#         Add the parent path to this object,
#         this triggers a rebuild of all the subitems in this object
#         """

#         self.Path = path+self.ID+"/"
#         for key in self.Subitem.keys():
#             self.Subitem[key].addPath(self.Path)

#     def getParent(self):
#         """
#         Returns the parent of this object
#         """

#         return self.__parent__

#     def setParent(self, parent):
#         """
#         Sets the parent of this object.
#         """

#         self.__parent__ = parent

#     def resetID(self):
#         """
#         Resets the ID and name of this object
#         """

#         self.ID = uuid.uuid1().hex
#         self.__name__ = self.ID

#     def paste(self, sourceobject):
#         """
#         The Paste method determines the type of the sourceobject to be pasted,
#         then makes a new object of that type and copies all the attributes to it.
#         This is then done recursively to its' subitems in the rebuild method.
#         It returns the object to be pasted.
#         """

#         # copiedsource = copy.deepcopy (sourceobject)
#         # copiedsource.setParent(self)
#         # self.rebuild (copiedsource)
#         # print copiedsource
#         # self.addItem(copiedsource.ID, copiedsource)
#         if isinstance(sourceobject, Project):
#             copiedsource = Project(sourceobject.Name, sourceobject.Description, sourceobject.getParent())
#         elif isinstance(sourceobject, BudgetGroup):
#             copiedsource = BudgetGroup(sourceobject.Name, sourceobject.Description, sourceobject.getParent())
#         else:
#             copiedsource = BudgetItem(sourceobject.Name, sourceobject.Description, sourceobject.Quantity, sourceobject.Rate, sourceobject.getParent())

#         copiedsource = self.rebuild(copiedsource, sourceobject.Subitem)
#         self.addItem(copiedsource.ID, copiedsource)

#     def rebuild(self, pastedsource, sourceobject):
#         """
#         Rebuild recursively creates a new object and copies all the attributes
#         to it and its children.
#         """

#         for key, value in sourceobject.items():
#             if isinstance(value, Project):
#                 copiedsource = Project(value.Name, value.Description, value.getParent())
#             elif isinstance(value, BudgetGroup):
#                 copiedsource = BudgetGroup(value.Name, value.Description, value.getParent())
#             else:
#                 copiedsource = BudgetItem(value.Name, value.Description, value.Quantity, value.Rate, value.getParent())

#             self.rebuild(copiedsource, value.Subitem)
#             pastedsource.addItem(copiedsource.ID, copiedsource)
#         return pastedsource

#     # def rebuild (self, copiedsource):
#     #     copiedsource.resetID()

#     #     for key, value in copiedsource.items():
#     #         value.setParent(copiedsource)
#     #         self.rebuild(value)

#     def __getitem__ (self, key):
#         """
#         Implement the __getitem__ method required for ZODB traversal
#         """

#         child = self.Subitem[key]

#         if child != None:
#             return child
#         else:
#             raise KeyError

#     def __str__(self):
#         """
#         The toString method returns a string of the name and
#         description of the class.
#         If the set is not empty thereafter it prints
#         all the items in the set.
#         """

#         output = self.Name + ": " + self.Description + ", " + self.ID + ", "
#         "" + self.Path
#         if self.Subitem is not None:
#             for key in self.Subitem.keys():
#                 output += ("\n\t" + str(self.Subitem[key]))

#         return output

class Parent(Base):
    """
    A Persistent class that acts as the root object in the ZODB
    It has an OOBTree of the children of this object
    It inherits from OptimateObject.
    """

    __tablename__ = 'Parent'
    ID = Column(Integer, primary_key=True)

class Children(Base):
    """
    A table of only the children of a parent
    """

    __tablename__ = 'Children'
    ID = Column(Integer, primary_key=True)
    ParentID = Column(Integer)


# class RootModel(OptimateObject):
#     """
#     A Persistent class that acts as the root object in the ZODB
#     It has an OOBTree of the children of this object
#     It inherits from OptimateObject.
#     """

#     __name__ = None
#     __parent__ = None

#     def __init__(self):
#         self.Subitem = OOBTree()
#         self.ID = "0"
#         self.Path = "/"

#     def __str__(self):
#         """
#         The toString method returns a string of the name and
#         description of the class.
#         If the set is not empty thereafter it prints
#         all the items in the set.
#         """

#         output = ""
#         if self.Subitem is not None:
#             for key in self.Subitem.keys():
#                 output += str(self.Subitem[key]) +"\n"

#         return output


class Project(Base):
    """
    A Persistent class that has the root as its parent
    It has an OOBTree of the children of this object
    It's ID is generated by uuid
    It inherits from OptimateObject.
    """

    __tablename__ = 'Projects'
    ID = Column(Integer, primary_key=True)
    Name = Column(Text)
    Description = Column(Text)



# class Project(OptimateObject):
#     """
#     A Persistent class that has the root as its parent
#     It has an OOBTree of the children of this object
#     It's ID is generated by uuid
#     It inherits from OptimateObject.
#     """

#     def __init__(self, nam, desc, parent):
#         self.Subitem = OOBTree()
#         self.Name = nam
#         self.Description = desc
#         self.ID = uuid.uuid1().hex    # The ID is the hex value of a UUID
#         self.__name__ = self.ID
#         self.__parent__ = parent
#         self.Path = ""

class BudgetGroup(Base):
    """
    A Persistent class that has a Project as its parent
    It has an OOBTree of the children of this object
    It's ID is generated by uuid
    It inherits from OptimateObject.
    """

    __tablename__ = 'BudgetGroups'
    ID = Column(Integer, primary_key=True)
    Name = Column(Text)
    Description = Column(Text)

# class BudgetGroup(OptimateObject):
#     """
#     A Persistent class that has a Project as its parent
#     It has an OOBTree of the children of this object
#     It's ID is generated by uuid
#     It inherits from OptimateObject.
#     """

#     def __init__(self, nam, desc, parent):
#         self.Subitem = OOBTree()
#         self.Name = nam
#         self.Description = desc
#         self.ID = uuid.uuid1().hex    # The ID is the hex value of a UUID
#         self.__name__ = self.ID
#         self.__parent__ = parent
#         self.Path = ""

class BudgetItem(Base):
    """
    A Persistent class that has a BudgetGroup as its parent
    Its the leaf object and has no children
    It's ID is generated by uuid
    It inherits from OptimateObject.
    """

    __tablename__ = 'BudgetItems'
    ID = Column(Integer, primary_key=True)
    Name = Column(Text)
    Description = Column(Text)
    Quantity = Column(Integer)
    Rate = Column(Integer)


# class BudgetItem(OptimateObject):
#     """
#     A Persistent class that has a BudgetGroup as its parent
#     Its the leaf object and has no children
#     It's ID is generated by uuid
#     It inherits from OptimateObject.
#     """

#     def __init__(self, nam, desc, quan, rate, parent):
#         self.Subitem = OOBTree()
#         self.Name = nam
#         self.Description = desc
#         self.Quantity = quan
#         self.Rate = rate
#         self.ID = uuid.uuid1().hex    # The ID is the hex value of a UUID
#         self.__name__ = self.ID
#         self.__parent__ = parent
#         self.Path = ""


# def appmaker(zodb_root):
#     """
#     appmaker gets the ZODB connection
#     and checks if there is anything in the root.
#     If there isn't then the database is built.
#     Afterward the root is returned.
#     """

    # if not 'app_root' in zodb_root:
    #     # Build the Root
    #     app_root = RootModel()

    #     # test if the datafile exists
    #     if os.path.exists("data.txt"):
    #         # Get data from the file
    #         projectlist = []
    #     # try:
    #         # Open the data file and read the first line.
    #         datafile = open("data.txt", "r")
    #         line = datafile.next().rstrip()

    #         # Iterate until the End Of File is reached.
    #         while line != "EOF":

    #             # "=" indicates the following is a Project structure
    #             if line == "=":
    #                 # Read the data and build the Project.
    #                 name = datafile.next().rstrip()
    #                 desc = datafile.next().rstrip()
    #                 project = Project(name, desc, app_root)

    #                 line = datafile.next().rstrip()
    #                 while line != "=" and line != "EOF":
    #                     # "+" indicates a BudgetGroup
    #                     if line == "+":
    #                         gname = datafile.next().rstrip()
    #                         gdesc = datafile.next().rstrip()
    #                         budgetgroup = BudgetGroup(gname, gdesc, project)
    #                         line = datafile.next().rstrip()

    #                         while line != "+" and line != "=":
    #                             # "*" indicates a BudgetItem
    #                             if line == "*":
    #                                 iname = datafile.next().rstrip()
    #                                 idesc = datafile.next().rstrip()
    #                                 iquantity = float(datafile.next().rstrip())
    #                                 irate = float(datafile.next().rstrip())

    #                                 budgetitem = BudgetItem(iname, idesc,
    #                                             iquantity, irate, budgetgroup)

    #                                 # Add the items to the BudgetGroup list.
    #                                 budgetgroup.addItem(budgetitem.ID,
    #                                                     budgetitem)
    #                                 line = datafile.next().rstrip()

    #                             # If the EOF is reached stop the iteration
    #                             if line == "EOF":
    #                                 break
    #                         # Add the BudgetGroup list to the Project list
    #                         project.addItem(budgetgroup.ID, budgetgroup)

    #                 projectlist.insert(len(projectlist), project)
    #         datafile.close()

    #         # Add the project and build the paths
    #         for project in projectlist:
    #             app_root.addItem(project.ID,project)

    #     # If it does not exist build the DB with hardcoded data
    #     else:
    #         #Build the Projects
    #         project = Node("PName", "PDesc", app_root)
    #         projectb = Node("BPName", "BPDesc", app_root)

    #         # Build the next level in the hierarchy
    #         budgetgroup = Node("BGName", "BGDesc", project)
    #         budgetgroupb = Node("BBGName", "BBGDesc", projectb)

    #         # Build the next level
    #         budgetitem = Leaf("BIName", "BIDesc", 10, 5, budgetgroup)
    #         budgetitemb = Leaf("BBIName", "BBIDesc", 4, 20, budgetgroupb)

    #         # Build the hierarchy
    #         budgetgroup.addItem(budgetitem.ID,budgetitem)
    #         project.addItem(budgetgroup.ID,budgetgroup)
    #         app_root.addItem(project.ID,project)

    #         budgetgroupb.addItem(budgetitemb.ID, budgetitemb)
    #         projectb.addItem(budgetgroupb.ID, budgetgroupb)
    #         app_root.addItem(projectb.ID, projectb)

    #     # Add the root the the ZODB
    #     zodb_root['app_root'] = app_root
    #     import transaction
    #     transaction.commit()
    # return zodb_root['app_root']
