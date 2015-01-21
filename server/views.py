"""
views.py sets up the view in the web file
it uses json as a renderer
the only response is a data structure containing a hierarchy
of the cost estimate items
"""

from pyramid.view import view_config
from pyramid.response import Response

@view_config(context='.models.RootModel', renderer='json')
def traversalview(context, request):

    # JSON expects the data to be a dictionary in a list
    JSONlist = [context.__dict__]
    return JSONlist
