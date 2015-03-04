"""
This scrip builds the SQLite DB used in this project and populates it with
default data.
"""

import os
import sys
import transaction
import uuid
from sqlalchemy import exc
from sqlalchemy.sql import exists
from pyramid.scripts.common import parse_vars
from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from ..models import (
    DBSession,
    Project,
    BudgetGroup,
    BudgetItem,
    Base,
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)

def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    # with transaction.manager:
    #     # Build the object models
    #     project = Project(Name="PName",
    #                         Description="PDesc",
    #                         ParentID='0')

    #     budgetgroup = BudgetGroup(Name="BGName",
    #                         Description="BGDesc",
    #                         ParentID=project.ID)

    #     budgetitem = BudgetItem(Name="BIName",
    #                         Description="BIDesc",
    #                         Quantity=10,
    #                         Rate=5,
    #                         ParentID=budgetgroup.ID)

    #     # Append the children nodes to their parents
    #     budgetgroup.Children.append(budgetitem)
    #     project.Children.append(budgetgroup)
    #     DBSession.add(project)


    #     projectb = Project(Name="BPName",
    #                         Description="BPDesc",
    #                         ParentID='0')

    #     budgetgroupb = BudgetGroup(Name="BBGName",
    #                         Description="BBGDesc",
    #                         ParentID=projectb.ID)

    #     budgetitemb = BudgetItem(Name="BBIName",
    #                         Description="BBIDesc",
    #                         Quantity=10,
    #                         Rate=5,
    #                         ParentID=budgetgroupb.ID)

    #     budgetgroupb.Children.append(budgetitemb)
    #     projectb.Children.append(budgetgroupb)
    #     DBSession.add(projectb)
