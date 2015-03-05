from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from server.models import (
    DBSession,
    Base,
    Node,
    Project,
    BudgetGroup,
    BudgetItem,
    )

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    ForeignKey,
    )

from random import randint
import sys
import transaction
from sqlalchemy import exc
from sqlalchemy.sql import exists
from pyramid.scripts.common import parse_vars
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
import xlrd
import uuid
import os

# delete the database
try:
    os.remove("server.sqlite")
except OSError, o:
    pass

config_uri = 'development.ini'
options = {}

settings = {'pyramid.includes': '\npyramid_debugtoolbar\npyramid_tm',
        'sqlalchemy.url': 'sqlite:////home/niel/projects/optimatesql/optimatesql/server.sqlite',
        '__file__': '/home/niel/projects/optimatesql/optimatesql/development.ini',
        'pyramid.default_locale_name': 'en', 'pyramid.reload_templates': 'true',
        'here': '/home/niel/projects/optimatesql/optimatesql',
        'pyramid.debug_notfound': 'false', 'pyramid.debug_routematch': 'false',
        'pyramid.debug_authorization': 'false'}

engine = engine_from_config(settings, 'sqlalchemy.')
session = DBSession
session.configure(bind=engine)
Base.metadata.create_all(engine)
with transaction.manager:

    """
    Open and read an Excel file
    """

    project = Project(ID=1, Name="test", Description="Desc", ParentID=0)
    bg = BudgetGroup(ID=2, Name="testbg", Description="bgdesc", ParentID=1)
    session.add(project)
    session.add(bg)
    qry =  session.query(Node).all()
    for n in qry:
        print n

    print session.query(BudgetGroup).filter_by(ID=2).update({'ID': 4})
    transaction.commit()
    qry =  session.query(Node).all()
    for n in qry:
        print n

    # projectbook = xlrd.open_workbook("/home/niel/projects/exceldata/Projects.xls")

    # first_sheet = projectbook.sheet_by_index(0)

    # codeindex = 0
    # nameindex = 1
    # descriptionindex = 2

    # # print "Converting Project table"
    # # # build the projects
    # for x in range (1, first_sheet.nrows):
    #     code = int(first_sheet.cell(x,codeindex).value)
    #     name = first_sheet.cell(x, nameindex).value
    #     description = first_sheet.cell(x, descriptionindex).value

    #     project = Project(ID=code, Name=name, Description=description, ParentID='0')
    #     session.add(project)

    # transaction.commit()

    # #build the budgetgroups
    # budgetgroupbook = xlrd.open_workbook("/home/niel/projects/exceldata/BudgetGroups.xls")

    # sheet = budgetgroupbook.sheet_by_index(0)
    # codeindex = 0
    # nameindex = 1
    # parentindex = 2
    # descriptionindex = 3

    # newcode = 150000
    # changedbgcodes = {}




    # print "Converting BudgetGroups table"
    # # build the budgetgroups
    # for x in range (1, sheet.nrows):
    #     code = int(sheet.cell(x,codeindex).value)
    #     name = sheet.cell(x, nameindex).value
    #     description = sheet.cell(x, descriptionindex).value
    #     try:
    #         parentcode = int(sheet.cell(x,parentindex).value)
    #     except ValueError, e:
    #         parentcode = 0

    #     # if the code has been changed assign it here
    #     if code in changedbgcodes.keys():
    #         code = changedbgcodes[code]

    #     # if it is negative it refers to a parent in the same table
    #     if parentcode < 0:
    #         parentcode = abs(parentcode)
    #         # test if the parent is already in the table
    #         parent = session.query(BudgetGroup).filter_by(ID=parentcode).first()
    #         if parent:
    #             # if it is in the table, change it's code and add it to the dict
    #             newcode+=1
    #             changedbgcodes[parentcode] = newcode
    #             temp = parentcode
    #             print "\nUpdate: "
    #             print session.query(BudgetGroup).filter_by(ID=parentcode).update({'ID': newcode})
    #             parentcode = newcode
    #             # parent = session.query(BudgetGroup).get(temp)
    #             # parent.ID = parentcode
    #             transaction.commit()

    #             print "old code: " + str(temp)
    #             print "new code: " + str (parentcode)
    #             print "old object: ",
    #             print session.query(BudgetGroup).filter_by(ID=temp).first()
    #             print "New object: ",
    #             print session.query(BudgetGroup).filter_by(ID=parentcode).first()
    #             # print session.query(BudgetGroup).filter_by(ID=parentcode).first().ID == newcode
    #         else:
    #             # if it is not in the table (None), add the code to the dict only
    #             newcode+=1
    #             changedbgcodes[parentcode] = newcode
    #             parentcode = newcode


    #     bg = BudgetGroup(ID=code, Name=name, Description=description, ParentID=parentcode)
    #     session.add(bg)

    # transaction.commit()
    # # # perform a separate query to change all negative parent codes
    # fixthese = session.query(Node.ParentID).filter(Node.ParentID>150000).all()
    # print len(fixthese)
    # # for pid in fixthese:
    # #     newcode+=1
    # #     session.query(Node).filter_by(ID=abs(pid[0])).update({'ID': newcode})
    # #     session.query(Node).filter_by(ParentID=pid[0]).update({'ParentID': newcode})


    # # transaction.commit()
    # qry =  session.query(BudgetGroup).all()
    # print len (qry)

    # print "building hierarchy"
    # # build it again adding the heirarchy
    # qry = session.query(BudgetGroup).all()
    # print len(qry)
    # for bg in qry:
    #     #get the id
    #     parentid = bg.ParentID
    #     # get the parent
    #     parent = session.query(Node).filter_by(ID=parentid).first()
    #     parent.Children.append(bg)



    # # session.commit()

    # #build the budgetitems
    # budgetitembook = xlrd.open_workbook("/home/niel/projects/exceldata/BudgetItems.xls")
    # sheet = budgetitembook.sheet_by_index(0)
    # codeindex = 0
    # nameindex = 1
    # parentindex = 2
    # descriptionindex = 3
    # quantityindex = 13
    # rateindex = 14

    # changedbicodes = {}

    # print "Converting Budgetitems table"
    # # build the budgetitems
    # for x in range (1, sheet.nrows):
    #     code = str(int(sheet.cell(x,codeindex).value))
    #     name = sheet.cell(x, nameindex).value
    #     description = sheet.cell(x, descriptionindex).value
    #     try:
    #         parentcode = int(sheet.cell(x,parentindex).value)
    #     except ValueError, e:
    #         parentcode = 0

    #     try:
    #         quantity = int(sheet.cell(x,quantityindex).value)
    #     except ValueError, e:
    #         quantity = 0

    #     try:
    #         rate = int(sheet.cell(x,rateindex).value)
    #     except ValueError, e:
    #         rate = 0


    #             # if the code has been changed assign it here
    #     if code in changedbicodes.keys():
    #         code = changedbicodes[code]

    #     # if it is negative it refers to a parent in the same table
    #     if parentcode < 0:
    #         parentcode = abs(parentcode)
    #         # test if the parent is already in the table
    #         parent = session.query(BudgetItem).filter_by(ID=parentcode).first()
    #         if parent:
    #             # if it is in the table, change it's code and add it to the dict
    #             newcode+=1
    #             changedbgcodes[parentcode] = newcode
    #             session.query(BudgetItem).filter(BudgetItem.ID == parentcode).update({'ID': newcode})
    #             parentcode = newcode
    #             # parent.ID = parentcode
    #             # session.commit()
    #         else:
    #             # if it is not in the table (None), add the code to the dict only
    #             newcode+=1
    #             changedbicodes[parentcode] = newcode
    #             parentcode = newcode

    #     bi = BudgetItem(ID=code, Name=name, Description=description, ParentID=parentcode, Quantity=quantity, Rate=rate)
    #     session.add(bi)

    # # session.commit()

    # print "Building hierarchy"
    # # build it again adding the heirarchy
    # qry = session.query(BudgetItem).all()
    # for bi in qry:
    #     #get the id
    #     parentid = bi.ParentID
    #     # get the parent
    #     parent = session.query(Node).filter_by(ID=parentid).first()
    #     parent.Children.append(bi)

    # # session.commit()



# for p in range(1, 11):
#     project = Project(Name="Project"+str(p), Description="projectdescription", ParentID='0')
#     print "adding: " + str(p)
#     # Build 100 budgetgroups
#     for bga in range(1, 11):
#         budgetgroupa = BudgetGroup(Name="BudgetGA"+str(bga), Description="bgadescription", ParentID=project.ID)

#         # Build 100 budgetgroups
#         for bgb in range(1, 11):
#             budgetgroupb = BudgetGroup(Name="BudgetGB", Description="bgbdescription", ParentID=budgetgroupa.ID)

#             # Build 1000 budgetitems
#             for bi in range(1, 11):
#                 budgetitem = BudgetItem(Name="BudgetItem", Description="bidescription", Quantity=randint(1, 100), Rate=randint(1, 100), ParentID=budgetgroupb.ID)
#                 budgetgroupb.Children.append(budgetitem)
#             # gc.collect()
#             budgetgroupa.Children.append(budgetgroupb)
#             # print "added to bg a"
#         # gc.collect()
#         project.Children.append(budgetgroupa)
#         # print "added to project: " + str(p)

#     session.add(project)
#     session.commit()

print "done"
