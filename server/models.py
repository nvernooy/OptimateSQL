"""
Models file contains resources used in the project
"""

import uuid
from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    ForeignKey,
    Float,
    )

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    backref,
    )

# Build the session and base used for the project
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension('changed')))
Base = declarative_base()

class Node(Base):
    """
    The Node class is an extrapolation of the objects used in this hierarchy.
    It has ID and ParentID attributes, the ParentID refers back to the ID
    of it's parent node.
    The ID of the node is generated by default using UUID.
    It also has a Children-Parent relationship attribute.
    """

    __tablename__ = 'Node'
    ID = Column(Integer, primary_key=True)
    ParentID = Column(Integer, ForeignKey('Node.ID', ondelete='CASCADE'))
    type = Column(Text(50))

    Children = relationship('Node',
                        cascade="all",
                        backref=backref("Parent", remote_side='Node.ID'),
                    )

    __mapper_args__ = {
        'polymorphic_identity':'Node',
        'polymorphic_on':type
        }

    def __repr__(self):
        return "<Node(ID='%s', ParentID='%s')>" % (
                self.ID, self.ParentID)

class Project(Node):
    """
    A table representing a Project in Optimate, it has an ID, Name, Description
    and ParentID that is the ID of its parent.
    It inherits from Node, and it's ID is linked to Node.ID
    It has copy and paste functions.
    It's total, ordered, and claimed attributes have properties that fire events
    """

    __tablename__ = 'Project'
    ID = Column(Integer, ForeignKey('Node.ID', ondelete='CASCADE'), primary_key=True)
    Name = Column(Text)
    Description = Column(Text)
    _Total = Column("Total", Float)
    _Ordered = Column("Ordered", Float)
    _Claimed = Column("Claimed", Float)

    __mapper_args__ = {
        'polymorphic_identity':'Project',
    }

    @hybrid_property
    def Total(self):
        if self._Total == None:
            self.recalculateTotal()
        return self._Total
    @Total.setter
    def Total(self, total):
        oldtotal = self.Total
        self._Total = total
        difference = total - oldtotal

        # update the parent with the new total
        if self.ParentID != 0:
            qry = DBSession.query(Node).filter_by(ID=self.ParentID).first()
            # if qry != None:
            try:
                qry.Total = qry.Total+difference
            except AttributeError, a:
                pass

    @hybrid_property
    def Ordered(self):
        if self._Ordered == None:
            self._Ordered = 0
        return self._Ordered
    @Ordered.setter
    def Ordered(self, ordered):
        self._Ordered = ordered

    @hybrid_property
    def Claimed(self):
        if self._Claimed == None:
            self._Claimed = 0
        return self._Claimed
    @Claimed.setter
    def Claimed(self, claimed):
        self._Claimed = claimed

    def copy(self, parentid):
        """
        copy returns an exact duplicate of this object,
        but with the ParentID specified.
        """

        copy = Project(Name=self.Name,
                        Description=self.Description,
                        ParentID=parentid)

        copy.Total=self.Total
        copy.Ordered=self.Ordered
        copy.Claimed=self.Claimed

        return copy


    def paste(self, source, sourcechildren):
        """
        paste appends a source object to the children of this node,
        and then recursively does the same with each child of the source object.
        """

        self.Children.append(source)

        for child in sourcechildren:
            source.paste(child.copy(source.ID), child.Children)

    def recalculateTotal(self):
        total = 0
        for item in self.Children:
            total+=item.Total

        self._Total = total
        return total

    def __repr__(self):
        return "<Node(Name='%s', ID='%s', ParentID='%s')>" % (
                            self.Name, self.ID, self.ParentID)

class BudgetGroup(Node):
    """
    A table representing a BudgetGroup in Optimate, it has an ID, Name,
    Description and ParentID that is the ID of its parent.
    It inherits from Node, and it's ID is linked to Node.ID
    It has copy and paste functions.
    """

    __tablename__ = 'BudgetGroup'
    ID = Column(Integer, ForeignKey('Node.ID', ondelete='CASCADE'), primary_key=True)
    Name = Column(Text)
    Description = Column(Text)
    _Total = Column("Total", Float)
    _Ordered = Column("Ordered", Float)
    _Claimed = Column("Claimed", Float)

    __mapper_args__ = {
        'polymorphic_identity':'BudgetGroup',
    }

    @hybrid_property
    def Total(self):
        if self._Total == None:
            self.recalculateTotal()
        return self._Total
    @Total.setter
    def Total(self, total):
        oldtotal = self.Total
        self._Total = total
        difference = total - oldtotal

        # update the parent with the new total
        # if self.ParentID != 0:
        #     qry = DBSession.query(Node).filter_by(ID=self.ParentID).first()
        #     # if qry != None:
        #     try:
        #         qry.Total = qry.Total+difference
        #     except AttributeError, a:
        #         pass

    @hybrid_property
    def Ordered(self):
        if self._Ordered == None:
            self._Ordered = 0
        return self._Ordered
    @Ordered.setter
    def Ordered(self, ordered):
        self._Ordered = ordered

    @hybrid_property
    def Claimed(self):
        if self._Claimed == None:
            self._Claimed = 0
        return self._Claimed
    @Claimed.setter
    def Claimed(self, claimed):
        self._Claimed = claimed

    def copy(self, parentid):
        """
        copy returns an exact duplicate of this object,
        but with the ParentID specified.
        """
        return BudgetGroup(Name=self.Name,
                            Description=self.Description,
                            ParentID=parentid)

        copy.Total=self.Total
        copy.Ordered=self.Ordered
        copy.Claimed=self.Claimed

        return copy
    def paste(self, source, sourcechildren):
        """
        paste appends a source object to the children of this node,
        and then recursively does the same with each child of the source object.
        """

        self.Children.append(source)

        for child in sourcechildren:
            source.paste(child.copy(source.ID), child.Children)

    def recalculateTotal(self):
        total = 0
        # if self.Total == None:
        #     self.recalculateAll()
        for item in self.Children:
            total+=item.Total

        self._Total = total
        return total

    def __repr__(self):
        return "<Node(Name='%s', ID='%s', ParentID='%s')>" % (
                         self.Name, self.ID, self.ParentID)


class BudgetItem(Node):
    """
    A table representing a BudgetItem in Optimate, it has an ID, Name,
    Description, Quantity, Rate and ParentID that is the ID of its parent.
    """

    __tablename__ = 'BudgetItem'
    ID = Column(Integer, ForeignKey('Node.ID', ondelete='CASCADE'), primary_key=True)
    Name = Column(Text)
    Description = Column(Text)
    Unit=Column(Text)
    _Quantity = Column("Quantity", Float)
    _Rate = Column("Rate", Float)
    _Total = Column("Total", Float)
    _Ordered = Column("Ordered", Float)
    _Claimed = Column("Claimed", Float)

    __mapper_args__ = {
        'polymorphic_identity':'BudgetItem',
    }

    @hybrid_property
    def Total(self):
        if self._Total == None:
            self.recalculateTotal()
        return self._Total
    @Total.setter
    def Total(self, total):
        oldtotal = self.Total
        self._Total = total
        difference = total - oldtotal

        # update the parent with the new total
        # if self.ParentID != 0:
        #     qry = DBSession.query(Node).filter_by(ID=self.ParentID).first()
        #     # if qry != None:
        #     try:
        #         qry.Total = qry.Total+difference
        #     except AttributeError, a:
        #         pass

    @hybrid_property
    def Ordered(self):
        if self._Ordered == None:
            self._Ordered = 0
        return self._Ordered
    @Ordered.setter
    def Ordered(self, ordered):
        self._Ordered = ordered

    @hybrid_property
    def Claimed(self):
        if self._Claimed == None:
            self._Claimed = 0
        return self._Claimed
    @Claimed.setter
    def Claimed(self, claimed):
        self._Claimed = claimed

    @hybrid_property
    def Rate(self):
        if self._Rate == None:
            self._Rate = 0
        return self._Rate
    @Rate.setter
    def Rate(self, rate):
        self._Rate = rate

        # change the total
        self.Total = self.Rate * self.Quantity

        # since the total has changed, change the rate of any parent
        # budgetitems
        qry = DBSession.query(BudgetItem).filter_by(ID=self.ParentID).first()
        if qry != None:
            qry.Rate = self.Total

    @hybrid_property
    def Quantity(self):
        if self._Quantity == None:
            self._Quantity = 0
        return self._Quantity
    @Quantity.setter
    def Quantity(self, quantity):
        self._Quantity = quantity

        # change the total
        self.Total = self.Rate * self.Quantity

        # since the total has changed, change the rate of any parent
        # budgetitems
        qry = DBSession.query(BudgetItem).filter_by(ID=self.ParentID).first()
        if qry != None:
            qry.Rate = self.Total

    def copy(self, parentid):
        """
        copy returns an exact duplicate of this object,
        but with the ParentID specified.
        """
        return BudgetItem(Name=self.Name,
                            Description=self.Description,
                            Unit=self.Unit,
                            ParentID=parentid)

        copy.Quantity=self.Quantity
        copy.Rate=self.Rate
        copy.Total=self.Total
        copy.Ordered=self.Ordered
        copy.Claimed=self.Claimed

        return copy

    def paste(self, source, sourcechildren):
        """
        paste appends a source object to the children of this node,
        and then recursively does the same with each child of the source object.
        """
        self.Children.append(source)

        for child in sourcechildren:
            source.paste(child.copy(source.ID), child.Children)

    def recalculateTotal(self):
        total = 0
        for item in self.Children:
            total+=item.Total

        total = total + self.Quantity*self.Rate
        self._Total = total
        return total


    def __repr__(self):
        return "<Node(Name='%s', ID='%s', ParentID='%s')>" % (
                            self.Name, self.ID, self.ParentID)

class Component(Node):

    __tablename__ = 'Component'
    ID = Column(Integer, ForeignKey('Node.ID', ondelete='CASCADE'), primary_key=True)
    Name = Column(Text)
    Description = Column(Text)
    Type = Column(Integer, ForeignKey('ComponentType.ID'))
    Unit = Column(Text)
    _Quantity = Column("Quantity", Float)
    _Rate = Column("Rate", Float)
    _Total = Column("Total", Float)
    _Ordered = Column("Ordered", Float)
    _Claimed = Column("Claimed", Float)

    __mapper_args__ = {
        'polymorphic_identity':'Component',
    }

    @hybrid_property
    def Total(self):
        if self._Total == None:
            self.recalculateTotal()
        return self._Total
    @Total.setter
    def Total(self, total):
        oldtotal = self.Total
        self._Total = total
        difference = total - oldtotal

        # update the parent with the new total
        # if self.ParentID != 0:
        #     qry = DBSession.query(Node).filter_by(ID=self.ParentID).first()
        #     # if qry != None:
        #     try:
        #         qry.Total = qry.Total+difference
        #     except AttributeError, a:
        #         pass

    @hybrid_property
    def Ordered(self):
        if self._Ordered == None:
            self._Ordered = 0
        return self._Ordered
    @Ordered.setter
    def Ordered(self, ordered):
        self._Ordered = ordered

    @hybrid_property
    def Claimed(self):
        if self._Claimed == None:
            self._Claimed = 0
        return self._Claimed
    @Claimed.setter
    def Claimed(self, claimed):
        self._Claimed = claimed

    @hybrid_property
    def Rate(self):
        if self._Rate == None:
            self._Rate = 0
        return self._Rate
    @Rate.setter
    def Rate(self, rate):
        self._Rate = rate

        # change the total
        self.Total = self.Rate * self.Quantity

        # since the total has changed, change the rate of any parent
        # budgetitems
        qry = DBSession.query(BudgetItem).filter_by(ID=self.ParentID).first()
        if qry != None:
            qry.Rate = self.Total

        qry = DBSession.query(Component).filter_by(ID=self.ParentID).first()
        if qry != None:
            qry.Rate = self.Total

    @hybrid_property
    def Quantity(self):
        if self._Quantity == None:
            self._Quantity = 0
        return self._Quantity
    @Quantity.setter
    def Quantity(self, quantity):
        self._Quantity = quantity

        # change the total
        self.Total = self.Rate * self.Quantity

        # since the total has changed, change the rate of any parent
        # budgetitems and components
        qry = DBSession.query(BudgetItem).filter_by(ID=self.ParentID).first()
        if qry != None:
            qry.Rate = self.Total

        qry = DBSession.query(Component).filter_by(ID=self.ParentID).first()
        if qry != None:
            qry.Rate = self.Total

    def copy(self, parentid):
        """
        copy returns an exact duplicate of this object,
        but with the ParentID specified.
        """
        return Component(Name=self.Name,
                            Description=self.Description,
                            Type=self.Type,
                            Unit=self.Unit,
                            ParentID=parentid)

        copy.Quantity=self.Quantity
        copy.Rate=self.Rate
        copy.Total=self.Total
        copy.Ordered=self.Ordered
        copy.Claimed=self.Claimed

        return copy


    def paste(self, source, sourcechildren):
        """
        paste appends a source object to the children of this node,
        and then recursively does the same with each child of the source object.
        """
        self.Children.append(source)

        for child in sourcechildren:
            source.paste(child.copy(source.ID), child.Children)

    def recalculateTotal(self):
        total = 0

        for item in self.Children:
            total+=item.Total

        total = total + self.Quantity*self.Rate
        self._Total = total
        return total

    def __repr__(self):
        return "<Node(Name='%s', ID='%s', ParentID='%s')>" % (
                            self.Name, self.ID, self.ParentID)


class ComponentType(Base):

    __tablename__ = 'ComponentType'
    ID = Column(Integer, primary_key=True)
    Name = Column(Text)

    Components = relationship('Component',
                            backref=backref('TypeOf'))

    def __repr__(self):
        return "<ComponentType(Name='%s', ID='%s')>" % (
                            self.Name, self.ID)

class ResourceCategory(Base):

    __tablename__ = 'ResourceCategory'
    Name = Column(Text, primary_key = True)
    Description = Column(Text)
    Rate = Column(Float)

    ResourceList = relationship('Resource',
                        cascade="all",
                        backref=backref("Category"),
                    )


    def __repr__(self):
        return "<ResourceCategory(Name='%s', Description='%s')>" % (
                            self.Name, self.Description)

class Resource(Base):

    __tablename__ = 'Resource'
    Name = Column(Text, ForeignKey('ResourceCategory.Name'))
    ID = Column(Integer, primary_key = True)
    ParentID = Column(Integer)

    # __mapper_args__ = {
    #     'polymorphic_identity':'Resource'
    #     }

    def __repr__(self):
        return "<Resource(Name='%s', ID='%s')>" % (
                            self.Name, self.ID)
