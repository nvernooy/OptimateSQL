"""
Models file contains resources used in the project
"""

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
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
    key = Column(Integer, primary_key=True)
    # ID = Column(Text, primary_key=True)
    ID = Column(Text)

class Project(Base):
    """
    A table representing a Project in Optimate, it has an ID, Name, Description
    and ParentID that is the ID of its parent.
    """

    __tablename__ = 'Project'
    key = Column(Integer, primary_key=True)
    # ID = Column(Text, primary_key=True)
    ID = Column(Text)
    Name = Column(Text)
    Description = Column(Text)
    ParentID = Column(Text)

class BudgetGroup(Base):
    """
    A table representing a BudgetGroup in Optimate, it has an ID, Name,
    Description and ParentID that is the ID of its parent.
    """

    __tablename__ = 'BudgetGroup'
    key = Column(Integer, primary_key=True)
    # ID = Column(Text, primary_key=True)
    ID = Column(Text)
    Name = Column(Text)
    Description = Column(Text)
    ParentID = Column(Text)

class BudgetItem(Base):
    """
    A table representing a BudgetItem in Optimate, it has an ID, Name,
    Description, Quantity, Rate and ParentID that is the ID of its parent.
    """

    __tablename__ = 'BudgetItem'
    key = Column(Integer, primary_key=True)
    # ID = Column(Text, primary_key=True)
    ID = Column(Text)
    Name = Column(Text)
    Description = Column(Text)
    Quantity = Column(Integer)
    Rate = Column(Integer)
    ParentID = Column(Text)
