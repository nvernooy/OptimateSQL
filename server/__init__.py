"""
__init__.py turns the directory into a package
and set the configuration for the server
"""

from pyramid.config import Configurator


def main(global_config, **settings):
    """Configure the requirements and html routes for the server."""

    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_route('Data', '/')
    config.scan('.views')
    return config.make_wsgi_app()
