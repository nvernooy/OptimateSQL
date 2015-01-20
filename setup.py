"""
setyp.py contains the set of modules required by this package
and sets up the development enviroment for pyramid
"""
import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

requires = [
    'pyramid',
    'pyramid_chameleon',
    'pyramid_zodbconn',
    'transaction',
    'ZODB3',
]

setup(name='server',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = server:main
      """,
)
