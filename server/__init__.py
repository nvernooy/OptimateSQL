"""
__init__.py turns the directory into a package
and set the configuration for the server
"""

from pyramid.config import Configurator
from pyramid.events import NewResponse
from pyramid.events import subscriber


@subscriber(NewResponse)
def handleResponse(event):
    """Create a new request factory,
    ensuring CORS headers on all json responses."""
    print "response event"

    if event.response.content_type == 'application/json':
        event.response.headers.update({
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Access-Control-Allow-Headers':
                event.request.headers.get('Access-Control-Request-Headers',
                'origin, accept, authorization'),
            'Access-Control-Allow-Credentials': 'true'})


def main(global_config, **settings):
    """Configure the requirements and html routes for the server."""

    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_route('Data', '/')
    config.scan('.views')
    return config.make_wsgi_app()
