"""
views.py sets up the view in the web file
it uses json as a renderer
the only response is a data structure containing a hierarchy of the cost estimate items
"""
 
from pyramid.view import (
    view_config,
    view_defaults
    )


@view_defaults(renderer='home.pt')
class TutorialViews:
    def __init__(self, request):
        self.request = request

    @view_config(route_name='Data', renderer='json')
    def OptimateData(self):
        return {'Project':	[{'ProjectName': 'A',
				'ProjectDesc': 'ADesc',
				'BudgetGroup':	[{'BudgetGroupName':'ABGName',
						'BudgetGroupDesc':'ABGDesc',
						'BudgetItem':	[{'BudgetItemName':'ABIName',
								'BudgetItemDesc':'ABIDesc',
								'BudgetItemQuantity':10,
								'BudgetItemRate':10
								}]
						}]
				},
				{'ProjectName': 'B',
				'ProjectDesc': 'BDesc',
				'BudgetGroup':	[{'BudgetGroupName':'B1BGName',
						'BudgetGroupDesc':'B1BGDesc',
						'BudgetItem':	[{'BudgetItemName':'B1BIName',
								'BudgetItemDesc':'B1BIDesc',
								'BudgetItemQuantity':10,
								'BudgetItemRate':10
								}]
						},
						{'BudgetGroupName':'B2BGName',
						'BudgetGroupDesc':'B2BGDesc',
						'BudgetItem':	[{'BudgetItemName':'B2.1BIName',
								'BudgetItemDesc':'B2.1BIDesc',
								'BudgetItemQuantity':10,
								'BudgetItemRate':10
								},
								{'BudgetItemName':'B2.2BIName',
								'BudgetItemDesc':'B2.1BIDesc',
								'BudgetItemQuantity':10,
								'BudgetItemRate':10
								}]
						}]

				}]
		}