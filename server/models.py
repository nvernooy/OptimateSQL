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
#     def getID():
#         return uuid.uuid1().hex


#     __tablename__ = 'Association'
    # ID = Column(Integer, primary_key=True, default=getID)
    # ID = Column(Text, primary_key=True, default=getID)
    # ParentID = Column(Integer)

    # child = relationship("Child", backref="parent_assocs")

class Node(Base):
    def getID():
        return uuid.uuid1().hex

    __tablename__ = 'Node'
    ID = Column(Text, primary_key=True, default=getID)
    ParentID = Column(Text, ForeignKey('Node.ID'))
    type = Column(Text(50))

    Children = relationship("Node",
                backref=backref('Parent', remote_side=[ID], uselist=False)
            )

    __mapper_args__ = {
        'polymorphic_identity':'Node',
        'polymorphic_on':type
    }

# class Root(Base):
#     """
#     A table in SQLite that only has the ID 0 and represents the root in the
#     hierarchy.
#     """

#     __tablename__ = 'Root'
#     ID = Column(Text, ForeignKey('Association.ID'), primary_key=True, default='0')

#     # Children = relationship("Project",
#     #                         backref='Parent',
#     #                         cascade="all, delete, delete-orphan")

#     def paste(self, source, sourcechildren):
#         DBSession.add(source)
#         DBSession.flush()

#         for child in sourcechildren:
#             source.paste(child.copy(source.ID), child.Children)


class Project(Node):
    """
    A table representing a Project in Optimate, it has an ID, Name, Description
    and ParentID that is the ID of its parent.
    """

    def getID():
        return uuid.uuid1().hex

    __tablename__ = 'Project'
    ID = Column(Text, ForeignKey('Node.ID'), primary_key=True)
    # ID = Column(Text, ForeignKey('Association.ID'), primary_key=True, default=getID)
    Name = Column(Text)
    Description = Column(Text)
    # ParentID = Column(Integer, ForeignKey('Association.ID'))

    __mapper_args__ = {
        'polymorphic_identity':'Project',
    }
    # AssociationID = relationship('Association',
    #                         foreign_keys='Project.ID',
    #                         backref='OptimateObject',
    #                         cascade='all, delete'
    #                         )

    # Parent = relationship('Association',
    #                         foreign_keys='Project.ParentID',
    #                         backref='Children',
    #                         cascade='all, delete'
    #                         )

    # Parent = relationship("Root",
    #                         backref='Children',
    #                         primaryjoin="and_(Project.ParentID==Root.ID)",
    #                         cascade="all, delete, delete-orphan")

    # Children = relationship("BudgetGroup",
    #                         backref='Parent',
    #                         cascade="all, delete, delete-orphan")

    # Parent = relationship('Association',
    #                         backref='Children',
    #                         cascade="all, delete")

    def copy(self, parentid):
        return Project(Name=self.Name, Description=self.Description, ParentID=parentid)

    def paste(self, source, sourcechildren):
        DBSession.add(source)
        DBSession.flush()

        for child in sourcechildren:
            source.paste(child.copy(source.ID), child.Children)


class BudgetGroup(Node):
    """
    A table representing a BudgetGroup in Optimate, it has an ID, Name,
    Description and ParentID that is the ID of its parent.
    """

    def getID():
        return uuid.uuid1().hex

    __tablename__ = 'BudgetGroup'
    # ID = Column(Text, ForeignKey('Association.ID'), primary_key=True, default=getID)
    ID = Column(Text, ForeignKey('Node.ID'), primary_key=True)
    Name = Column(Text)
    Description = Column(Text)
    # ParentID = Column(Integer, ForeignKey('Association.ID'))

    __mapper_args__ = {
        'polymorphic_identity':'BudgetGroup',
    }
    # AssociationID = relationship('Association',
    #                         foreign_keys='BudgetGroup.ID',
    #                         backref='OptimateObject',
    #                         cascade='all, delete'
    #                         )
    # Parent = relationship('Association',
    #                         foreign_keys='BudgetGroup.ParentID',
    #                         backref='Children',
    #                         cascade='all, delete'
    #                         )

    # Parent = relationship("Project",
    #                         primaryjoin="and_(BudgetGroup.ParentID==Project.ID)",
    #                         backref='Children',
    #                         cascade="all, delete, delete-orphan")

    # Children = relationship("BudgetItem",
    #                         backref='Parent',
    #                         cascade="all, delete, delete-orphan")

    # Parent = relationship("Association",
    #                         backref='Children',
    #                         cascade="all, delete")

    def copy(self, parentid):
        return BudgetGroup(Name=self.Name, Description=self.Description, ParentID=parentid)

    def paste(self, source, sourcechildren):
        DBSession.add(source)
        DBSession.flush()

        for child in sourcechildren:
            source.paste(child.copy(source.ID), child.Children)

class BudgetItem(Node):
    """
    A table representing a BudgetItem in Optimate, it has an ID, Name,
    Description, Quantity, Rate and ParentID that is the ID of its parent.
    """

    def getID():
        return uuid.uuid1().hex

    __tablename__ = 'BudgetItem'
    # ID = Column(Text, ForeignKey('Association.ID'), primary_key=True, default=getID)
    ID = Column(Text, ForeignKey('Node.ID'), primary_key=True)
    Name = Column(Text)
    Description = Column(Text)
    Quantity = Column(Integer)
    Rate = Column(Integer)
    # ParentID = Column(Integer, ForeignKey('Association.ID'))

    __mapper_args__ = {
        'polymorphic_identity':'BudgetItem',
    }
    # AssociationID = relationship('Association',
    #                         foreign_keys='BudgetItem.ID',
    #                         backref='OptimateObject',
    #                         cascade='all, delete'
    #                         )
    # Parent = relationship('Association',
    #                         foreign_keys='BudgetItem.ParentID',
    #                         backref='Children',
    #                         cascade='all, delete'
    #                         )

    # Children = [] #relationship("BudgetItem",
                #            backref='Parent',
                 #           cascade="all, delete, delete-orphan")

    # Parent = relationship("Association",
    #                         backref='Children',
    #                         cascade="all, delete")

    def copy(self, parentid):
        return BudgetItem(Name=self.Name, Description=self.Description, Quantity=self.Quantity, Rate=self.Rate, ParentID=parentid)

    def paste(self, source, sourcechildren):
        DBSession.add(source)
        DBSession.flush()

        for child in sourcechildren:
            source.paste(child.copy(source.ID), child.Children)
