"""
__init__.py turns the directory into a package
and set the configuration for the server
"""

# from pyramid.config import Configurator
from pyramid.events import NewResponse
from pyramid.events import subscriber
from pyramid.events import NewRequest
# from pyramid_zodbconn import get_connection
# from models import appmaker

from pyramid.config import Configurator
from sqlalchemy import engine_from_config


from .models import (
    DBSession,
    Base,
    )


# def root_factory(request):
#     """Make the ZODB connection and get the root from appmaker."""
#     conn = get_connection(request)
#     return appmaker(conn.root())


@subscriber(NewResponse)
def handleResponse(event):
    """Create a new request factory,
    ensuring CORS headers on all json responses."""

    def cors_headers(request, response):
        response.headers.update({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST,GET,DELETE,PUT,OPTIONS',
        'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization',
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Max-Age': '1728000',
        })
    event.request.add_response_callback(cors_headers)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_subscriber(handleResponse, NewRequest)
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('root', '/')
    config.scan('.views')
    return config.make_wsgi_app()
