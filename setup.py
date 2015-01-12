"""
setyp.py contains the set of modules required by this package
and sets up the development enviroment for pyramid
"""

from setuptools import setup

requires = [
    'pyramid',
    'pyramid_chameleon',
]

setup(name='server',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = server:main
      """,
)
