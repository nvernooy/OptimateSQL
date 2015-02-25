"""
Models file contains resources used in the project
"""

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    ForeignKey,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    backref,
    )

from zope.sqlalchemy import ZopeTransactionExtension

import uuid

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

# class Association(Base):
#     __tablename__ = 'Association'
#     Parent = Column(Integer, ForeignKey('left.id'), primary_key=True)
#     Child = Column(Integer, ForeignKey('right.id'), primary_key=True)
#     extra_data = Column(String(50))
#     child = relationship("Child", backref="parent_assocs")

class Root(Base):
    """
    A table in SQLite that only has the ID 0 and represents the root in the
    hierarchy.
    """

    __tablename__ = 'Root'
    ID = Column(Integer, primary_key=True)

    Children = relationship("Project",
                            backref='Parent',
                            cascade="all, delete, delete-orphan")

    def paste(self, source, sourcechildren):
        DBSession.add(source)
        DBSession.flush()

        for child in sourcechildren:
            source.paste(child.copy(source.ID), child.Children)


class Project(Base):
    """
    A table representing a Project in Optimate, it has an ID, Name, Description
    and ParentID that is the ID of its parent.
    """

    def getID():
        return uuid.uuid1().hex

    __tablename__ = 'Project'
    ID = Column(Text, primary_key=True, default=getID)
    Name = Column(Text)
    Description = Column(Text)
    ParentID = Column(Integer, ForeignKey('Root.ID'))

    # Parent = relationship("Root",
    #                         backref='Children',
    #                         primaryjoin="and_(Project.ParentID==Root.ID)",
    #                         cascade="all, delete, delete-orphan")

    Children = relationship("BudgetGroup",
                            backref='Parent',
                            cascade="all, delete, delete-orphan")

    def copy(self, parentid):
        return Project(Name=self.Name, Description=self.Description, ParentID=parentid)

    def paste(self, source, sourcechildren):
        DBSession.add(source)
        DBSession.flush()

        for child in sourcechildren:
            source.paste(child.copy(source.ID), child.Children)


class BudgetGroup(Base):
    """
    A table representing a BudgetGroup in Optimate, it has an ID, Name,
    Description and ParentID that is the ID of its parent.
    """

    def getID():
        return uuid.uuid1().hex

    __tablename__ = 'BudgetGroup'
    ID = Column(Text, primary_key=True, default=getID)
    Name = Column(Text)
    Description = Column(Text)
    ParentID = Column(Integer, ForeignKey('Project.ID'))

    # Parent = relationship("Project",
    #                         primaryjoin="and_(BudgetGroup.ParentID==Project.ID)",
    #                         backref='Children',
    #                         cascade="all, delete, delete-orphan")

    Children = relationship("BudgetItem",
                            backref='Parent',
                            cascade="all, delete, delete-orphan")

    def copy(self, parentid):
        return BudgetGroup(Name=self.Name, Description=self.Description, ParentID=parentid)

    def paste(self, source, sourcechildren):
        DBSession.add(source)
        DBSession.flush()

        for child in sourcechildren:
            source.paste(child.copy(source.ID), child.Children)

class BudgetItem(Base):
    """
    A table representing a BudgetItem in Optimate, it has an ID, Name,
    Description, Quantity, Rate and ParentID that is the ID of its parent.
    """

    def getID():
        return uuid.uuid1().hex

    __tablename__ = 'BudgetItem'
    ID = Column(Text, primary_key=True, default=getID)
    Name = Column(Text)
    Description = Column(Text)
    Quantity = Column(Integer)
    Rate = Column(Integer)
    ParentID = Column(Integer, ForeignKey('BudgetGroup.ID'))

    Children = [] #relationship("BudgetItem",
                #            backref='Parent',
                 #           cascade="all, delete, delete-orphan")

    def copy(self, parentid):
        return BudgetItem(Name=self.Name, Description=self.Description, Quantity=self.Quantity, Rate=self.Rate, ParentID=parentid)

    def paste(self, source, sourcechildren):
        DBSession.add(source)
        DBSession.flush()

        for child in sourcechildren:
            source.paste(child.copy(source.ID), child.Children)
