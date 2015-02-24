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

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

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

class Project(Base):
    """
    A table representing a Project in Optimate, it has an ID, Name, Description
    and ParentID that is the ID of its parent.
    """

    __tablename__ = 'Project'
    ID = Column(Integer, primary_key=True)
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


class BudgetGroup(Base):
    """
    A table representing a BudgetGroup in Optimate, it has an ID, Name,
    Description and ParentID that is the ID of its parent.
    """

    __tablename__ = 'BudgetGroup'
    ID = Column(Integer, primary_key=True)
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

class BudgetItem(Base):
    """
    A table representing a BudgetItem in Optimate, it has an ID, Name,
    Description, Quantity, Rate and ParentID that is the ID of its parent.
    """

    __tablename__ = 'BudgetItem'
    ID = Column(Integer, primary_key=True)
    Name = Column(Text)
    Description = Column(Text)
    Quantity = Column(Integer)
    Rate = Column(Integer)
    ParentID = Column(Integer, ForeignKey('BudgetGroup.ID'))

    # Parent = relationship("BudgetGroup",
    #                         primaryjoin="and_(BudgetItem.ParentID==BudgetGroup.ID)",
    #                         backref='Children',
    #                         cascade="all, delete, delete-orphan")
